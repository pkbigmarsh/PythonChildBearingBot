import sys
import socket
import string
import os

from basic_bot import *
from child_bearer_bot import *


HOST='irc.accessirc.net'
PORT=6667
NICK='ChildBearingBot'
IDENT='ChildBearingBot'
REALNAME='ChildBearingBot'
OWNER='msumwalt'
CHANNELINIT='#BotTesting'
readbuffer=''

botChildren = []

PythonBot = ChildBearer(HOST, NICK, OWNER, CHANNELINIT)
PythonBot.run()