#!/usr/bin/env python3

import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

TARGET_APP = 'com.hoge.app'

jscode = """
Module.enumerateExports("libcocos2dcpp.so", {                
    onMatch: function(e) {                            
        if(e.type == 'function' && e.name.indexOf('aes_initializeDecrypt') > -1){
            console.log("name of function = " + e.name);
            console.log("address = " + e.address);                                                        
        }    
    },                                                
    onComplete: function() {}                         
});  
"""

process = frida.get_usb_device().attach(TARGET_APP)
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running')
script.load()
