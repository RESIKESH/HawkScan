# -*- coding: utf-8 -*-
#Thanks Jamb0n69 !

import socketio
import time
import os, sys
import traceback
import argparse
import json

# External
from config import PLUS, WARNING, INFO, LESS, LINE, FORBI, BACK


socketio_paths = [
            "socket.io", "socketio", "io", "socket", "signalr", "xmpp-websocket", "websocket"
        ]


class check_socketio:
    """
    check_socketio: Check socketio connection without authentification. Possible found message, logs or other traces
    """

    sio = socketio.Client(reconnection=False)
    dynamic_function_number = 0



    def connect(self, url, path):
        try:
            #print(url+path) #DEBUG
            self.sio.connect(url, socketio_path=path)
            return True
        except Exception as e:
            #print(e) #DEBUG
            if "www." in url:
                urli = url.replace("www.","")
                self.connect(urli, path)
            return e
        return False

    def disconnect(self):
        try:
            self.sio.disconnect()
        except:
            pass


    def run_socketio(self, url, poutput):
        found_socket = False
        if poutput:
            print(LINE)
            print("{} Check for websockets".format(INFO))
            print(LINE)
        for path in socketio_paths:
            connect = self.connect(url, path)
            if type(connect) == bool and connect == True:
                print(" {} {}{} found !".format(PLUS, url, path))
                domain = url.split("/")[2] if not "www" in url else ".".join(url.split("/")[2].split(".")[1:])
                print(" {} Try this \"\033[36msudo apt install npm -y && npx wscat -c ws://{}/socket.io/?transport=websocket\033[0m\" \n If you have a 30X redirection you can try with 'wss://'".format(INFO, domain))
                self.disconnect()
                found_socket = True
            elif not found_socket and poutput:
                print(" {} {}{}: {}".format(LESS, url, path, connect))
        if not found_socket:
            print("\n {} Nothing Socketio found".format(LESS))


    def main_socketio(self, url):
        if "www." in url:
            urls = []
            urls.append(url)
            urls.append(url.replace("www.", ""))
            for u in urls:
                print("{} {}".format(INFO, u))
                self.run_socketio(u, poutput=False)
        else:
            self.run_socketio(url, poutput=True)


"""if __name__ == '__main__':
    url = sys.argv[1]

    check_socketio = check_socketio()
    check_socketio.run_socketio(url)"""