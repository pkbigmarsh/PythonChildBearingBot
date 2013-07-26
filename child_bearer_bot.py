from basic_bot import *
from child_bot import *
import socket
import select

class ChildBearer(BasicBot):
	def __init__(this, host, nick, channel_list):
		BasicBot.__init__(this, host, nick, channel_list)
		this.children = []
		this.sockets = [this.sock]

	def create_bot(this, msg):
		print '!! --- Creating Child --- !!'
		nick = this.parseUser(msg) + "_jr"
		hasChild = False
		for child in this.children:
			if child.NICK == nick:
				hasChild = True
		if hasChild == False:
			target, message = this.parsePRIVMSG(msg)
			child_bot = ChildBot(this.HOST, nick, target)
			this.children.append(child_bot)
			this.sockets.append(child_bot.sock)
			child_bot.connect();

	def handle_messages(this, msg):
		if 'child' in msg:
			this.create_bot(msg)

	def run(this):
		this.sock.connect((this.HOST, this.PORT))
		this.sock.send('NICK ' + this.NICK + '\n')
		this.sock.send('USER ' + this.IDENT + ' ' + this.HOST + ' bla :' + this.REALNAME + '\n')

		while 1:
			ready_to_read, ready_to_write, in_error = select.select(this.sockets, [], [])
			if this.sock in ready_to_read:
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
				if(child.sock in ready_to_read):
					line2 = child.sock.recv(500)
					if len(line2) > 0:
						print 'Child --- ' + child.NICK + '::' + line2
					child.basic_message_handle(line2)