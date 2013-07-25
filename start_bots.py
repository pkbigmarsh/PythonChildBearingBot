import sys
import socket
import string
import os

from BotChild import *


HOST='colorscience.lpdev.prtdev.lexmark.com'
PORT=6667
NICK='PythonBot2221'
IDENT='P'
REALNAME='Marshall'
OWENER='msumwalt'
CHANNELINIT='#msumwaltTest'
readbuffer=''

botChildren = []

PythonBot = bot_child(HOST, NICK, IDENT, REALNAME, CHANNELINIT)
PythonBot.run()

Bot2 = bot_child(HOST, 'Bot22', 'MBOT', 'MBOT2', 'MarshallS', CHANNELINIT)
Bot2.run()