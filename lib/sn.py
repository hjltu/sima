#!/usr/bin/env python3

"""
sn.py
https://github.com/hjltu/sima
author: hjltu@ya.ru, license: MIT/X11

last change: 24-feb-19

python3 sn.py 00000000c6c99a95 26299095
serial number to password
drop all zeros and convert
"abcdef" to hexadecimal and
shift 10 (a=0,b=1..f=5)
"""

import sys


def main(sn=None):
    passwd = ""
    for i in str(sn):
        if i is not "0":
            if i.isdigit():
                passwd += i
            else:
                try:
                    passwd += str(int(i, 16)-10)
                except Exception as e:
                    return "ERR "+str(e)
    return passwd

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1]))
    except:
        sys.exit(1)
