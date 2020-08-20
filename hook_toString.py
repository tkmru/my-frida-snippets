#!/usr/bin/env python3

import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

TARGET_APP = 'com.hoge.app'

jscode = """
Java.perform(function () {
  var JavaString = Java.use('java.lang.String');
  var StringBuilder = Java.use('java.lang.StringBuilder');
  var toString = StringBuilder.toString;
  toString.implementation = function () {
    var result = JavaString.$new('10000000');
    return result;
  };
  console.log('[+] toString() hooked');
});
"""

process = frida.get_usb_device().attach(TARGET_APP)
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running')
script.load()
sys.stdin.read()
