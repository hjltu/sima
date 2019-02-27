#!/usr/bin/env python3

"""
dialog.py
https://github.com/hjltu/sima
author: hjltu@ya.ru, license: MIT/X11

last change: 24-feb-19
"""

import csv
import random
try:
    from . import mytext
    from . import mydb
    from . import accessory
except:
    import mytext
    import mydb
    import accessory


# skip comment string in csv file
def decomment(csvfile):
    """ delete a line started with '#' """

    for row in csvfile:
        raw = row.split('#')[0].strip()
        if raw: yield raw


# get PRi serial numbers from csv files
def get_sn(mydir,myfiles):
    """
    input:
        mydir - client directory name,
        myfiles - files to check and parse.
    output:
        list of client's RPi serial numbers.
    """

    sn =[]
    for f in myfiles:
        try:
            with open(mydir + "/" + f, newline="") as csvfile:
                reader = csv.reader(decomment(csvfile))
                sn.append(next(reader)[1])
        except:
            return "ERR read csv's"
    return sn


# parse csv file from clients dir
def get_accessories(serNum, mydir, myfiles):
    """
    input:
        serNum - RPi serial number,
        mydir - client directory name,
        myfiles - files to check and parse.
    output:
        list[n][3] of accessories.
    """

    acc = []
    for f in myfiles:
        try:
            with open(mydir + "/" + f) as csvfile:
                reader = csv.reader(decomment(csvfile))
                acc = list(reader)
        except:
            return "ERR read csv's"
        # check serial number and delete first row with that number
        if serNum.strip() == acc[0][1]:
            del acc[0]
            return acc


# common dialogues
def common(msg, comm):
    """
    input:
        msg - POST input/output dict,
        comm - command from msg.
    output:
        msg - with processed response.
    """


    # if ping
    if comm != "ping":
        print("comm:",comm)
    if "ping" in comm:
        msg["response"]["text"] = random.choice(mytext.pong)
        msg["response"]["tts"] = random.choice(mytext.pong)
        msg["response"]["end_session"] = True
        print("\u001b[2A")  # 2 times up

    # if Alisa in command
    if "алиса" in comm:
        msg["response"]["text"] = random.choice(mytext.alisa)
        msg["response"]["tts"] = random.choice(mytext.alisa)

    # exit
    if len([x for x in mytext.end if x in comm]) > 0:
        msg["response"]["text"] = random.choice(mytext.end).capitalize()
        msg["response"]["tts"] = random.choice(mytext.end)
        msg["response"]["end_session"] = True

    return msg


def my_welcome(msg, uid, comm):
    """
    input:
        msg - POST input/output dict,
        uid - device ID
        comm - command from msg.
    output:
        msg - with processed response.
    """


    # greetings
    if mytext.welcome in comm:
        if uid is None:
            msg["response"]["text"] = mytext.welcome + mytext.new
            msg["response"]["tts"] = mytext.welcome+" --------------- "+mytext.new
        else:
            msg["response"]["text"] = mytext.welcome
            msg["response"]["tts"] = mytext.welcome

    # help
    if any(w in comm for w in mytext.hlp):
        if uid is None:
            msg["response"]["text"] = mytext.new + mytext.newPass
            msg["response"]["tts"] = mytext.new +" --------------- "+mytext.newPass
        else:
            msg["response"]["text"] = mytext.helpForClients
            msg["response"]["tts"] = mytext.helpForClients

    return msg


# check password
def check_passwd(comm):
    """
    input:
        comm - string contains password
    output:
        passwd - password, str.
    """

    passwd = ""
    for i in comm:
        if i.isdigit():
            passwd += i
    if len(passwd) == 8:
        return passwd
    return None


def my_user(msg,userId,comm):
    pass

















