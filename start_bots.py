import sys
import socket
import string
import os

from basic_bot import *
from child_bearer_bot import *


HOST='colorscience.lpdev.prtdev.lexmark.com'
PORT=6667
NICK='ChildBearingBot'
IDENT='ChildBearingBot'
REALNAME='ChildBearingBot'
OWNER='msumwalt'
CHANNELINIT='#msumwaltTesting'
readbuffer=''

botChildren = []

PythonBot = ChildBearer(HOST, NICK, CHANNELINIT)
PythonBot.run()