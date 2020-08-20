#!/usr/bin/env python3
import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


TARGET_APP = 'com.hoge.app'
TARGET_CLASS = "com.hoge.app.MainActivity$1"

process = frida.get_usb_device().attach(TARGET_APP)
jscode = """
Java.performNow(function() {
  Java.choose('""" + TARGET_CLASS + """', {
    onMatch: function(instance) {
      console.log(Object.getOwnPropertyNames(instance.__proto__));             
    }, onComplete: function() {
      console.log("[*] Completed");
    }
    onEnter: function (log, args, state) {
      for(var i=0; i<10; i++) {
        log("Func args[" + i + "]" + Memory.readUtf8String(args[i]));
      }
    },

  });
});
"""

script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running')
script.load()
