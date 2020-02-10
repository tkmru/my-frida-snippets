#!/usr/bin/env python3

import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

jscode = """
Java.perform(function() {
  Java.enumerateLoadedClasses({
	  onMatch: function(className) {
	    console.log(className);
	  },
	  onComplete: function() {
	    console.log("[*] Completed");
	  }
  });
});
"""

TARGET_APP = 'com.hoge.app'
process = frida.get_usb_device().attach(TARGET_APP)
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running')
script.load()
