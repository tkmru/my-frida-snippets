#!/usr/bin/env python3

import frida, sys

TARGET_APP = 'com.hoge.app'
FUNC_NAME = 'hoge'

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

jscode = """
Interceptor.attach(Module.getExportByName('libhoge.so', '""" + FUNC_NAME + """'), {
    onEnter: function(args) {
        console.log('args: ')
        for(var j=0; j<8; j++){
            console.log("arg[" + j + "]: " + args[j]);
        }
        console.log(Memory.readCString(args[1]));
    },
    onLeave: function(retval) {
        console.log('retval: ')
        console.log(retval)
    }
});
"""

process = frida.get_usb_device().attach(TARGET_APP)
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running')
script.load()
sys.stdin.read()
