from basic_bot import *
import time

class ChildBot(BasicBot):
	def __init__(this, host, nick, channel_list):
		BasicBot.__init__(this, host, nick, channel_list)
		this.lifespan = 100

	def handle_messages(this, msg):
		print this.nick