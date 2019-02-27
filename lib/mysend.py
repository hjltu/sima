#!/usr/bin/env python3

"""
send-command.py
https://github.com/hjltu/sima
author: hjltu@ya.ru, license: MIT/X11

send command to local MQTT server

usage:
    python3 hjclient.py 000000002254753d test 123
"""

import sys
import time
import json
import paho.mqtt.client as mqtt

# encription
import socket
import ssl


RTOPIC = "/hjconnect/"
SERVER = "localhost"
PORT = 1883


def my_json(payload):
    return json.dumps(payload)  # object2string


def main(ID, TOP, MSG):
    client = mqtt.Client()
    client.connect(SERVER, PORT, 60)
    client.loop_start()
    top = RTOPIC + ID + "/in"
    comm = "mosquitto_pub -t /homekit/" + TOP + " -m " + str(MSG)
    msg = {
        "in": comm,
        "err": "", "time": time.time()}
    print("top:",top,"comm:",comm)
    client.publish(top, my_json(msg))
    time.sleep(2)
    client.loop_stop()


if __name__ == "__main__":
    if len(sys.argv) == 4:
        ID = sys.argv[1]
        TOP = sys.argv[2]
        MSG = sys.argv[3]
        main(ID, TOP, MSG)
    else:
        sys.exit(1)
