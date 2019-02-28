#!/usr/bin/env python3

"""
sima.py
Навык Робот Сима
https://github.com/hjltu/sima
author: hjltu@ya.ru, license: MIT/X11

yandex:
https://tech.yandex.ru/dialogs/alice
https://dialogs.yandex.ru/developer/

ssl crt:
openssl req -new -keyout server.pem -out server.pem -x509 -days 365 -nodes -subj '/CN=site.com/O=user/C=RU'

lib/sn.py RPi serial to password

clients/my.csv Home automation hjmqtt
https://github.com/hjltu/hjmqtt

lib/mysend.py send MQTT command to hjconnect
https://github.com/hjltu/hjconnect

usage:
    python3 sima.py [-t],[-test]

last change: 24-feb-19
"""

# coding: utf-8
# from __future__ import unicode_literals

import json
import cgi
import ssl
import random
import time
import os
import sys
import threading
from lib import mysend
from lib import mytext
from lib import accessory
from lib import mydb
from lib import dialog
from lib import sn

# http
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading


# create and test db
mydb.create()
if mydb.select() == 2:
    mydb.insert()

# user_id and sn, dict
users = mydb.select_all()
if type(users) is not dict:
    print("ERR in db, exit")
    sys.exit(1)

# load clients data
# client's dirname, string
MYDIR = mytext.clientsDir

# list filenames in client's dir
isfile = os.path.isfile
join = os.path.join
myfiles = [f for f in os.listdir(MYDIR) if isfile(join(MYDIR, f))]
print(myfiles)

# list RPi serial numbers
mysn = dialog.get_sn(MYDIR, myfiles)
if "ERR" in mysn:
    sys.exit(1)
print(mysn)

# create accessories
Lt = accessory.Light()
Rl = accessory.Rele()
Dm = accessory.Dimmer()
Ct = accessory.Curtains()
Tr = accessory.Term()

#sys.exit(0)

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("get")
        self.send_response(200)
        self.end_headers()
        message =  threading.currentThread().getName()
        message += '\nHi! I am Robot Sima, i live here.'
        self.wfile.write(message.encode())
        self.wfile.write('\n'.encode())
        return

    def do_POST(self):
        # print("post")
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        # refuse if not json
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            print("ERR: json header")
            return

        # check input json
        try:
            # json to dict
            length = int(self.headers.get('content-length'))
            msg = json.loads(self.rfile.read(length).decode("utf-8"))
            # command, str
            comm = msg["request"]["command"].lower()
            # device ID, str
            userId = msg["session"]["user_id"]
        except:
            print("ERR: not json")
            return
        try:
            # default answer
            msg = {"response": {"text": mytext.ans,
                    "tts": mytext.ans,
                    "end_session": False},
                "session": {"session_id": msg["session"]["session_id"],
                    "message_id": msg["session"]["message_id"],
                    "user_id": msg["session"]["user_id"]},
                "version": "1.0"}
            #msg["response"]["tts"] = mytext.ans
        except:
            print("ERR: wrong json")
            return

        # when json is OK, general Q&A session
        if len(comm) == 0:
            comm = mytext.welcome
        msg = dialog.common(msg, comm)

        # global variables defines out of class
        global users
        global myfiles
        global mysn
        global MYDIR

        # check new user device,
        # add new ID in db and users, check result
        if userId not in users:
            out = mydb.insert(name=userId)
            if out == 0:
                users[userId] = None
                print("add new id")
                msg["response"]["text"] = random.choice(mytext.done)
                msg["response"]["tts"] = random.choice(mytext.done)
            else:
                print("ERR: mydb.insert return",out)
                msg["response"]["text"] = random.choice(mytext.err)
                msg["response"]["tts"] = random.choice(mytext.err)

        # add or remove RPi serial
        if mytext.myPass in comm or mytext.myDel in comm:
            # check password
            passwd = dialog.check_passwd(comm)
            if passwd:
                for s in mysn:
                    if sn.main(s) == passwd:   # selial to password
                        # add new password
                        if mytext.myPass in comm:
                            out = mydb.update(name=userId, stat=passwd)
                            if out == 0:
                                users = mydb.select_all()
                                print("add sn")
                                msg["response"]["text"] = random.choice(mytext.done)
                                msg["response"]["tts"] = mytext.harp + random.choice(mytext.done)
                            else:
                                msg["response"]["text"] = random.choice(mytext.err)
                                msg["response"]["tts"] = random.choice(mytext.err)
                        # remove password
                        if mytext.myDel in comm:
                            out = mydb.update(name=userId)
                            if out == 0:
                                users[userId] = None
                                print("remove sn")
                                msg["response"]["text"] = random.choice(mytext.done)
                                msg["response"]["tts"] = random.choice(mytext.done)
                            else:
                                msg["response"]["text"] = random.choice(mytext.err)
                                msg["response"]["tts"] = random.choice(mytext.err)

        # welcome new user
        msg = dialog.my_welcome(msg, users[userId], comm)
        # for registered users
        if users[userId]:
            serNum = None
            passwd = mydb.select(name=userId)
            for s in mysn:
                if sn.main(s) == passwd:
                    serNum = s
            # Hooray! Home automation section
            if serNum:
                accessories = dialog.get_accessories(serNum, MYDIR, myfiles)
                print(accessories)
                for acc in accessories:
                    if acc[1] == "rele":
                        out = Rl.action(comm, acc[0], acc[2])
                    if acc[1] == "light":
                        out = Lt.action(comm, acc[0], acc[2])
                    if acc[1] == "dimm":
                        out = Dm.action(comm, acc[0], acc[2])
                    if acc[1] == "curt":
                        out = Ct.action(comm, acc[0], acc[2])
                    if acc[1] == "term":
                        out = Tr.action(comm, acc[0], acc[2])
                    if type(out) == dict:
                        msg["response"]["text"] = random.choice(mytext.done)
                        msg["response"]["tts"] = mytext.sw + random.choice(mytext.done)
                        for k in out:
                            threading.Thread(target=mysend.main, args=(serNum, k, out[k])).start()

        # We did it!
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(msg).encode())


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


#def my_user(msg, userId):
#    return msg


if __name__ == "__main__":
    print("Start ",time.strftime("%d-%b-%y_%H:%M:%S"),"\n")
    try:
        if sys.argv[1] == "-t" or sys.argv[1] == "-test":
            server = ThreadedHTTPServer(('localhost', 8000), Handler)
    except:
        server = HTTPServer(("0.0.0.0", 8000), Handler)
        server.socket = ssl.wrap_socket( server.socket, certfile='./crt.pem', server_side=True )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    print("exit")
