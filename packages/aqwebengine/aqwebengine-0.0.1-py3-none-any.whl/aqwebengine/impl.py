import json
import uuid
import functools
import asyncio
import inspect
import sys
from .qtx import QIODevice, QFile, QWebEngineView, QWebEngineScript, QWebChannel, Slot, QObject, QUrl, QWebEngineSettings


def _read_from_resource(resource_url):
    f = QFile(resource_url)
    if not f.open(QIODevice.ReadOnly):
        raise RuntimeError('Failed to open resource: ' + resource_url)

    try:
        return bytes(f.readAll()).decode('utf-8')
    finally:
        f.close()


_QT_WEBCHANNEL = _read_from_resource(':/qtwebchannel/qwebchannel.js')


def _script(name, js, injectionPoint=QWebEngineScript.DocumentReady):
    s = QWebEngineScript()
    s.setSourceCode(js)
    s.setName(name)
    s.setWorldId(QWebEngineScript.MainWorld)
    s.setInjectionPoint(injectionPoint)
    s.setRunsOnSubFrames(True)
    return s


class _Bridge(QObject):
    def __init__(self, call_python, js_eval, on_js_eval_reply):
        super().__init__()
        self._call_python = call_python
        self._js_eval = js_eval
        self._on_js_eval_reply = on_js_eval_reply

    @Slot(str, str)
    def call_python(self, caller_id, json_string):
        '''This method facilitates async communication from JS to Python'''

        async def handle(json_string):
            return await self._call_python(json.loads(json_string))

        def done_callback(caller_id, task):
            try:
                result = {
                    'result': task.result(),
                }
            except BaseException as err:
                result = {
                    'error': str(err),
                }
            result = json.dumps(result)
            self._js_eval(f'window.qt._pythonReply({repr(caller_id)}, {repr(result)});')

        task = asyncio.create_task(handle(json_string))
        task.add_done_callback(functools.partial(done_callback, caller_id))

    @Slot(str, str)
    def js_reply(self, caller_id, json_string):
        '''This method facilitates async communication from Python to JS'''
        asyncio.create_task(self._on_js_eval_reply(caller_id, json_string))


class JSError(RuntimeError): pass


_APP_JS = '''(() => {
    if (window.qt === undefined) {
        return;
    }

    const locals = { callId: 0 };

    const reply = { };

    new QWebChannel(window.qt.webChannelTransport, channel => {
        window.qt.callPython = (name, params) => {
            const callId = locals.callId++;
            const promise = new Promise( (resolve, reject) => {
                reply['' + callId] = { resolve, reject };
                channel.objects.bridge.call_python('' + callId, JSON.stringify({ name, params }));
            });
            return promise;
        };

        window.qt._pythonReply = (callId, valueAsJsonString) => {
            const promise = reply['' + callId];
            delete reply['' + callId];
            const value = JSON.parse(valueAsJsonString);
            if (value.error) {
                return promise.reject(value.error);
            } else {
                return promise.resolve(value.result);
            }
        };

        window.qt._jsReply = (callId, value) => {
            channel.objects.bridge.js_reply('' + callId, JSON.stringify(value));
        }

        window.qt.callPython('bridge-is-ready');
    });
})();
'''

class AQWebEngineView(QWebEngineView):

    def set_font_family(self, family):
        '''Convenience shortcut to set default font name'''
        self.page().settings().setFontFamily(QWebEngineSettings.StandardFont, family)

    def set_font_size(self, size):
        '''Convenience shortcut to set default font size'''
        self.page().settings().setFontSize(QWebEngineSettings.DefaultFontSize, size)

    def __init__(self, *av, **kav):
        super().__init__(*av, **kav)

        self._channel = QWebChannel()
        self.page().setWebChannel(self._channel)

        self._bridge = _Bridge(self._call_python, self.page().runJavaScript, self._on_eval_js_reply)
        self._channel.registerObject('bridge', self._bridge)

        self._reply = {}
        self._reply_ready = asyncio.Condition()

        self._set_content_lock = asyncio.Lock()

        self._registered_python_functions = {}

        self._inited = asyncio.Event()

    async def init(self):
        '''Initialize 2-way communication machinery between Python host and JS guest'''

        if self._inited.is_set():
            raise RuntimeError('alreadey inited')

        self.page().profile().scripts().insert(
            _script(
                'QtWebChannel.js',
                _QT_WEBCHANNEL + '\n' + _APP_JS,
                injectionPoint=QWebEngineScript.DocumentCreation
            )
        )

        self.setHtml('')

        await self._inited.wait()

    async def eval_js(self, js_script):
        '''Calls JS guest, evaluating the string.

        String can be any valid JS expression, evaluating to a value or promise. One particularly
        convenient idiom is to use self-evaluating function block, example:

            js_script = """(async ()=>{
                const response = await fetch("https://www.google.com");
                return await response.text();
            })()"""
        '''
        if not self._inited.is_set():
            raise RuntimeError('Not inited. Did you forget to call "await init()" on me?')

        id_ = str(uuid.uuid4())
        async with self._reply_ready:
            self.page().runJavaScript(f'''(async () => {{
                try {{
                    const value = await Promise.resolve(eval({repr(js_script)}));
                    return {{
                        id: "{id_}",
                        value: value,
                    }};
                }} catch(err) {{
                    console.error('ERR: ' + err);
                    return {{
                        id: "{id_}",
                        error: 'JS: ' + err,
                    }};
                }}
            }})().then(value => qt._jsReply("{id_}", value));''')
            while True:
                if id_ in self._reply:
                    value = self._reply.pop(id_)
                    if value.get('error') is not None:
                        raise JSError(value['error'])
                    return value.get('value')
                try:
                    await self._reply_ready.wait()
                except asyncio.exceptions.CancelledError:
                    return None

    async def _on_eval_js_reply(self, caller_id, json_string):
        params = json.loads(json_string)
        async with self._reply_ready:
            self._reply[caller_id] = params
            self._reply_ready.notify_all()

    def register_python_function(self, name, async_callable):
        '''Register python function to expose it to the JS callers.

        Function should take a single argument of any JSON-serializable type. It can be sync or async.

        Example:

            w = QWebEngineView()
            await w.init()

            def f(message):
                print(message)
                return 42

            w.register_python_function('my_function_name', f)
            w.page().runJavaScript("""( async () => {
                const response = await window.qt.callPython("my_function_name", "Hello, world");
                console.error("Python function my_function_name returned", response);
            })()""")

        '''
        self._registered_python_functions[name] = async_callable

    async def _call_python(self, event):
        if event['name'] == 'bridge-is-ready':
            self._inited.set()
        elif event['name'] in self._registered_python_functions:
            afn = self._registered_python_functions[event['name']]
            result = afn(event['params'])
            if inspect.iscoroutine(result):
                result = await result
            return result
        else:
            raise RuntimeError(f'Python function {event["name"]} is not registered')

    async def set_html_async(self, html, base_url=None):
        '''Loads HTML text, asynchronously'''
        async with self._set_content_lock:
            f = asyncio.Future()
            def handler(success):
                if success:
                    f.set_result(None)
                else:
                    f.set_exception(RuntimeError('set_html_async() failed'))
            self.loadFinished.connect(handler)
            try:
                if base_url is not None:
                    self.setHtml(html, QUrl(base_url))
                else:
                    self.setHtml(html)
                await f
            finally:
                self.loadFinished.disconnect(handler)

    async def load_async(self, url):
        '''Loads URL, asynchronously'''
        async with self._set_content_lock:
            f = asyncio.Future()
            def handler(success):
                if success:
                    f.set_result(None)
                else:
                    f.set_exception(RuntimeError(f'load_async("{url}") failed'))
            self.loadFinished.connect(handler)
            try:
                import os
                self.load(QUrl(url))
                await f
            finally:
                self.loadFinished.disconnect(handler)

    async def to_html_async(self):
        '''Retrieve current page source, as HTML'''
        f = asyncio.Future()
        self.page().toHtml(f.set_result)
        await f
        return f.result()

    async def to_plain_text_async(self):
        '''Retrieve current page source, as plain text'''
        f = asyncio.Future()
        self.page().toPlainText(f.set_result)
        await f
        return f.result()


def async_slot(fn):
    '''Wrapper for async functions to make them synchronous. Qt signals can only connect to synchronous functions.

    Example:

        @async_slot
        async def do_something():
            await asyncio.sleep(10)

        ...
        push_button.clicked.connect(do_something)
    '''

    @functools.wraps(fn)
    def wrapper(*av, **kav):
        def handle_done(task):
            try:
                task.result()
            except asyncio.exceptions.CancelledError:
                pass
            except Exception:
                sys.excepthook(*sys.exc_info())

        task = asyncio.create_task(fn(*av, **kav))
        task.add_done_callback(handle_done)

    return wrapper


if __name__ == '__main__':
    HTML = '''
<html xml:lang="en" xmlns="http://www.w3.org/1999/xhtml">
	<head>

		<meta charset="utf-8" />

        <link href="styles/red.css" rel="stylesheet" type="text/css" />

        <link href="styles/focus.css" rel="stylesheet" type="text/css" />

        <title> </title>

        <link href="styles/redwok.css" rel="stylesheet" />

    </head>

<body id="body" red-id="body">
    <div class="chapter" id="sec-1" red-id="sec-1">
        <h1 id="pz1-1" red-id="pz1-1">
            <span bbox="211.37 690.45 400.63 714.54" id="z1-1" pg="1" red-id="z1-1">Redwok Sample </span>
        </h1>

        <div class="image" id="pz1-2" red-id="pz1-2">
            <img alt="images/img-AP.png" bbox="73.50 356.82 541.50 666.57" class="image" id="AP" pg="1" src="images/img-AP.png" />
        </div>

        <p id="pz1-3" red-id="pz1-3">
            <span bbox="72.00 326.82 200.12 335.86" id="z1-3" pg="1" red-id="z1-3">Font type “Courier” </span>
        </p>

        <p id="pz1-4" red-id="pz1-4">
            <span bbox="72.00 295.34 154.64 306.68" id="z1-4" pg="1" red-id="z1-4">Font type “Lora” </span>
        </p>

        <table id="pz1-5" red-id="pz1-5">
            <tbody grid-x="72.00 150.41 262.53 385.64 540.50" grid-y="192.00 215.84 238.66 264.50" id="z1-5" pg="1" rotation="0">
                <tr id="tr-z1-5-0">
                    <td id="td-z1-5-0-0">
                        <span bbox="72.00 238.66 150.41 264.50" id="std-z1-5-0-0" pg="1">Name </span>
                    </td>
                    <td id="td-z1-5-0-1">
                        <span bbox="150.41 238.66 262.53 264.50" id="std-z1-5-0-1" pg="1">Age </span>
                    </td>
                    <td id="td-z1-5-0-2">
                        <span bbox="262.53 238.66 385.64 264.50" id="std-z1-5-0-2" pg="1">Height </span>
                    </td>
                    <td id="td-z1-5-0-3">
                        <span bbox="385.64 238.66 540.50 264.50" id="std-z1-5-0-3" pg="1">Weight </span>
                    </td>
                </tr>
                <tr id="tr-z1-5-1">
                    <td id="td-z1-5-1-0">
                        <span bbox="72.00 215.84 150.41 238.66" id="std-z1-5-1-0" pg="1">Joe </span>
                    </td>
                    <td id="td-z1-5-1-1">
                        <span bbox="150.41 215.84 262.53 238.66" id="std-z1-5-1-1" pg="1">32 </span>
                    </td>
                    <td id="td-z1-5-1-2">
                        <span bbox="262.53 215.84 385.64 238.66" id="std-z1-5-1-2" pg="1">5’ 9” </span>
                    </td>
                    <td id="td-z1-5-1-3">
                        <span bbox="385.64 215.84 540.50 238.66" id="std-z1-5-1-3" pg="1">200 lb </span>
                    </td>
                </tr>
                <tr id="tr-z1-5-2">
                    <td id="td-z1-5-2-0">
                        <span bbox="72.00 192.00 150.41 215.84" id="std-z1-5-2-0" pg="1">Mary </span>
                    </td>
                    <td id="td-z1-5-2-1">
                        <span bbox="150.41 192.00 262.53 215.84" id="std-z1-5-2-1" pg="1">30 </span>
                    </td>
                    <td id="td-z1-5-2-2">
                        <span bbox="262.53 192.00 385.64 215.84" id="std-z1-5-2-2" pg="1">5’ 5” </span>
                    </td>
                    <td id="td-z1-5-2-3">
                        <span bbox="385.64 192.00 540.50 215.84" id="std-z1-5-2-3" pg="1">150 lb </span>
                    </td>
                </tr>
            </tbody>
        </table>

        <p id="pz1-6" red-id="pz1-6">
            <span bbox="72.00 164.48 278.54 174.80" id="z1-6" pg="1" red-id="z1-6">Lets do some colored font: <color id="A4" rgb="#980000" style="color: rgb(152,0,0);">red</color> <color id="AO" rgb="#37751c" style="color: rgb(55,117,28);">green</color> <color id="A3" rgb="#1154cb" style="color: rgb(17,84,203);">blue</color>. </span>
        </p>

        <p id="pz1-7" red-id="pz1-7">
            <span bbox="72.00 135.51 208.24 146.62" id="z1-7" pg="1" red-id="z1-7">Lorem ipsum<sup>1</sup> dolos rectum. </span>
        </p>

        <p id="pz1-8" red-id="pz1-8">
            <span bbox="72.00 106.29 384.23 116.61" id="z1-8" pg="1" red-id="z1-8">Some inline links to <color id="AR" rgb="#1154cb" style="color: rgb(17,84,203);"><u id="Ai">http: //www.google.com</u></color>, gopher: //coo.boo.at. </span>
        </p>

        <p class="footnote" id="pz1-9" red-id="pz1-9">
            <span bbox="72.00 74.00 216.00 88.87" id="z1-9" pg="1" red-id="z1-9"><sup>1</sup> This is footnote </span>
        </p>

        <p id="pz2-1" red-id="pz2-1">
            <span bbox="72.00 707.50 228.41 717.69" id="z2-1" pg="2" red-id="z2-1">Lorem ipsum link to Section 1.1. </span>
        </p>
        </div>
    </body>
</html>
'''
    # https://github.com/spyder-ide/spyder/issues/3226#issuecomment-316021155
    import ctypes
    ctypes.CDLL("libGL.so.1", mode=ctypes.RTLD_GLOBAL)

    import asyncio
    import functools
    import sys
    from PyQt5.QtWidgets import QPushButton

    def main_wrapper(main):
        @functools.wraps(main)
        async def wrapper(*av, **kaw):
            f = asyncio.Future()
            qasync.QApplication.instance().aboutToQuit.connect(f.cancel)

            result = await main(*av, **kaw)

            try:
                await f
            except asyncio.exceptions.CancelledError:
                pass

            return result
        return wrapper

    @main_wrapper
    async def main():
        base = QWebEngineView()
        await base.init()
        await base.set_html_async(HTML)

        base.loadStarted.connect(functools.partial(print, 'loadStarted'))
        base.loadFinished.connect(functools.partial(print, 'loadFinished'))
        base.loadProgress.connect(functools.partial(print, 'loadProgredd'))

        base.show()
        button = QPushButton('hitme')
        async def hitme(_):
            await base.load_async('https://www.google.com')
            # base.page().runJavaScript('app.callPython("xx", "").then(value => {console.error("VAL:" + value);}).catch(err => {console.error("ERR:" + err)})')
            # out = await base.runJavaScript('Zoo=3')
            # print(out)
            out = await base.eval_js('(async () => { console.error(fetch); return 3; }) ()')
            print(out)
            raise ValueError('here')
            # await base._loadResource(RESOURCES_ROOT_URL + '/red/inject.js')
            # await base._loadResource(RESOURCES_ROOT_URL + '/red/shortcut.js')
        button.clicked.connect(asyncSlot(hitme))
        button.show()

        return locals()

    # print(_QT_WEBCHANNEL)

    import qasync
    qasync.run(main())
