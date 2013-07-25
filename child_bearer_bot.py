from basic_bot import *

class ChildBearer(BasicBot):
	def __init__(this, host, nick, owner, channel_list):
		BasicBot.__init__(this, host, nick, owner, channel_list)
		this.children = []

	def handle_mssages(this, msg):
		print 'Mother'

	def run(this):
		this.sock.connect((this.HOST, this.PORT))
		this.sock.send('NICK ' + this.NICK + '\n')
		this.sock.send('USER ' + this.IDENT + ' ' + this.HOST + ' bla :' + this.REALNAME + '\n')

		while 1:
			line = this.sock.recv(500)
			if len(line) > 0:
				print line
			if line.find("Welcome") != -1:
				this.join(this.CHANNEL_LIST)
			elif line.find("PRIVMSG") != -1:
				this.hangle_messages(line)
			elif line.find('PING') != -1:
				this.pingPong(line)