#!/usr/bin/env python3

import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


if len(sys.argv) < 3:
    print('Usage: %s <begin address> <end address>' % sys.argv[0])
    sys.exit(1)

TARGET_APP = 'com.hoge.app'
begin_addr = int(sys.argv[1], 16)
end_addr = int(sys.argv[2], 16)
length = end_addr - begin_addr

jscode = """
var pointer = new NativePointer('""" + str(begin_addr) + """');
var buf = Memory.readByteArray(pointer, """ + str(length) + """);
console.log(hexdump(buf, {
  offset: 0,
  length: """ + str(length) + """,
  header: true,
  ansi: true
}));
"""

process = frida.get_usb_device().attach(TARGET_APP)
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running')
script.load()
