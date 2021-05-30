from inspect import signature

class SocketMessages():
    def __init__(self, sio, window):
        self.window = window
        self.sio = sio

        @sio.on('OUTPUT')
        def output_message(b):
            self.exec("output", b)

        @sio.on('ANALOG')
        def analog_message(b):
            self.exec("input", b, lambda d: self.emit_report("ANALOG_MESSAGE", b['index'], d))

        @sio.on('SERVO')
        def servo_message(b):
            self.exec("servo", b)

        @sio.on('PIN')
        def servo_message(b):
            self.exec("pin", b)

        @sio.on('PIXEL')
        def servo_message(b):
            self.exec("pixel", b)

    def emit_report(self, key, index, data):
        self.sio.start_background_task(target=self.emit(key, {'index': index, 'value': data}))

    def emit(self, key, value):
        self.sio.emit(key, value)

    def exec(self, obj, data, callback=False):
        print('Received data: ', data)
        if not self.pre(): return
        o = getattr(self.window.i, obj)
        f = getattr(o(data['index']), data['method'])
        sig = signature(f)
        params = list(sig.parameters.values())
        try:
            if len(sig.parameters) == 0:
                f()
            elif len(sig.parameters) == 1:
                if callback:
                    f(callback)
                else:
                    # checkear si vienen los parametros opcionales
                    if not ('param' in data) and not (params[0].default is params[0].empty):
                        data['param'] = params[0].default
                    f(data['param'])
            elif len(sig.parameters) == 2:
                # checkear si vienen los parametros opcionales
                if not ('param2' in data) and not (params[1].default is params[1].empty):
                    data['param2'] = params[1].default
                f(data['param'], data['param2'])
            elif len(sig.parameters) == 3:
                # checkear si vienen los parametros opcionales
                if not ('param2' in data) and not (params[1].default is params[1].empty):
                    data['param2'] = params[1].default
                if not ('param3' in data) and not (params[2].default is params[2].empty):
                    data['param3'] = params[2].default
                f(data['param'], data['param2'], data['param3'])
            self.log(self.window.i.lastMsg)
        except Exception as inst:
            self.log("No se ha podido ejecutar el comando: "+obj)
            print(inst)

    def log(self, msg):
        self.window.consoleTrigger.emit(msg)

    def pre(self):
        if not hasattr(self.window, "i"):
            self.log("No hay interfaz conectada")
            return False
        if not self.window.i:
            self.log("No hay interfaz conectada")
            return False
        return True