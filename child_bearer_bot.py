from basic_bot import *
from child_bot import *

class ChildBearer(BasicBot):
	def __init__(this, host, nick, owner, channel_list):
		BasicBot.__init__(this, host, nick, owner, channel_list)
		this.children = []

	def create_bot(this, message):
		child_bot = ChildBot(this.HOST, 'Child1', this.OWNER, this.CHANNEL_LIST)
		child_bot.connect()
		this.children.append(child_bot)
		print len(this.children)

	def handle_messages(this, msg):
		user = this.parseUser(msg)
		sender, message = this.parsePRIVMSG(msg)
		if message.find('Create bot ') != -1:
			this.create_bot(message)

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
				this.handle_messages(line)
			elif line.find('PING') != -1:
				this.pingPong(line)

			for child in this.children:
				line2 = child.sock.recv(500)
				child.basic_message_handle(line2)