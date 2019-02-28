#!/usr/bin/env python3

"""
accessory.py
https://github.com/hjltu/sima
author: hjltu@ya.ru, license: MIT/X11

last change 24-feb-19

check accessory name and return
topic and payload

usage:
import accessory

My = accessory.Light()

My.action("включи свет", "кухн", "kux")
My.action("включи кухню, "кухн", "kux"")
My.action("включи всё, "кухн", "kux"")

output is dict:
{"kux": 1}
"""

import time
try:
    from . import mytext
except:
    import mytext


class Start(object):

    def __init__(self):
        pass

    total = mytext.total

    def check_total(self, text):
        """ all same type accesories"""
        if(any(t in self.total for t in text.split()) or
            any(t in self.types for t in text.split())):
            return True
        return False

    def check_name(self, text, name):
        """ check accessory name """
        if name in text:
            return True
        else:
            return False

    def act_dimm(self, out, text, top, dimm=None):
        """ for 0-100 values """
        proc = ""
        for t in text.split():
            if t.isdigit():
                proc += t
        if proc is not "":
            if int(proc) < 0 or int(proc) > 100:
                return
            out={}
            if dimm:
                out[top+dimm] = float(proc)*2.54
            else:
                out[top] = proc
        return out


class Light(Start):
    """ on/off accessory """

    on = mytext.onLight
    off = mytext.offLight
    types = mytext.light

    def on_off(self, text, top):
        """ return dict {topic: payload} """
        if self.on in text:
            return {top: 1}
        if self.off in text:
            return {top: 0}

    def action(self, text, name, top):
        """ on/off lights """
        if(self.check_total(text) == False and
            self.check_name(text, name) == False):
            return
        return self.on_off(text, top)


class Rele(Light):
    on = mytext.onRele
    off = mytext.offRele
    types = mytext.rele


class Dimmer(Light):
    """ on/off and 0-100% ligth """

    def action(self, text, name, top):
        """ return dict {topic: payload, topic-dimm: payload} """
        if(self.check_total(text) == False and
            self.check_name(text, name) == False):
            return
        out = self.on_off(text, top)
        if out:
            return self.act_dimm(out, text, top, dimm="-dimm")


class Curtains(Start):
    """ on/off and 0-100% ligth """

    op = mytext.openCurt
    cl = mytext.closeCurt
    types = mytext.curtains

    def open_close(self, text, top):
        """ return dict {topic: payload} """
        if self.op in text:
            return {top: 100}
        if self.cl in text:
            return {top: 0}

    def action(self, text, name, top):
        """ return dict {topic-dimm: payload} """
        if(self.check_total(text) == False and
            self.check_name(text, name) == False):
            return
        out = self.open_close(text, top)
        if out:
            return self.act_dimm(out, text, top)


class Sensor(Start):
    """ Temp, Hum, Motion, Leak """

    def action(self, text, name, top):
        print(name)


class Term(Start):
    """ Thermoreg """

    types = mytext.termoreg

    def action(self, text, name, top):
        """ return dict {topic-dimm: payload} """
        if(self.check_total(text) == False and
            self.check_name(text, name) == False):
            return
        out = self.act_dimm({top: ""}, text, top, dimm="-target")
        try:
            out[top+"-target"] /= 2.54
            if out[top+"-target"] >= 10 and out[top+"-target"] <= 35:
                return out
        except:
            print("ERR in Term")
