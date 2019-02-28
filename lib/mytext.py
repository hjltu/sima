#!/usr/bin/env python3

"""
mytext.py
https://github.com/hjltu/sima
author: hjltu@ya.ru, license: MIT/X11
"""


clientsDir = "clients"

# welcome
welcome = "Привет "

# help for new user
hlp = ["помощ","что ты умеешь"]
new = "Я выполняю команды для управления приборами домашней автоматики, \
    например: \"Включи свет на кухне\" или \"Гости\" \
    для выхода скажите \"пока\""

helpForClients = "Команды для управления освещением: \
    \"включить\" или \"отключить,\" \
    для управления шторами: \"открыть\" \"закрыть,\" \
    для управления терморегуляторами: \"установить температуру,\" \
    для управления другими приборами: \"подключить\" \"отключить\""

newPass = "Для активации назовите пароль?"
myPass = "пароль"
myDel = "удалить"

# request
total = ["все","всё","везде","весь"]

# Light, Dimmer
light = "свет"
onLight = "включ"
offLight = "выключ"

# Rele
rele = "прибор"
onRele = "подключ"
offRele = "отключ"

# Curtains
curtains = "шторы"
openCurt = "откр"
closeCurt = "закр"

# Term
termoreg = "температур"

# answer
pong = ["pong","Ку-ку"]
ans = "Я это не умею"
done = ["Готово", "Сделано"]
err = ["Ошибка","Попробуйте ещё раз"]
scene = ["Выполняю сценарий"]
end = ["пока","конец","выход"]
alisa = ["Алиса отошла","Какая ещё Алиса?"]

# effects
sw = '<speaker audio="alice-sounds-things-switch-1.opus">'
harp = '<speaker audio="alice-music-harp-1.opus">'
