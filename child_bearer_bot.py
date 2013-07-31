from basic_bot import *
from child_bot import *
import socket
import select
from threading import Timer

class ChildBearer(BasicBot):
	def __init__(this, host, nick, channel_list):
		BasicBot.__init__(this, host, nick, channel_list)
		this.children = []
		this.sockets = [this.sock]
		this.isAbleToBear = False;
		this.childTimer = Timer(10, this.update_child_bearing)
		this.childTimer.start()
		this.max_children = 2

	def create_bot(this, msg):
		print '!! --- Creating Child --- !!'
		mommy = this.parseUser(msg)
		nick = mommy + "_jr"
		hasChild = False
		for child in this.children:
			if child.NICK == nick:
				hasChild = True
		if hasChild == False:
			target, message = this.parsePRIVMSG(msg)
			child_bot = ChildBot(this.HOST, nick, target, mommy)
			this.children.append(child_bot)
			this.sockets.append(child_bot.sock)
			child_bot.connect();
			return True
		else:
			return False

	def handle_messages(this, msg):
		user = this.parseUser(msg)
		target, message = this.parsePRIVMSG(msg)
		if 'child' in msg and this.isAbleToBear == True and len(this.children) < this.max_children:
			if this.create_bot(msg):
				this.isAbleToBear = False
				this.childTimer = Timer(10, this.update_child_bearing)
				this.childTimer.start()
			else:
				this.message(target, user + ' don\'t be greedy')
		elif 'child' in msg and this.isAbleToBear == False and len(this.children) < this.max_children:
			this.message(target, user + ' you can\'t have a child');
		elif 'child' in msg and len(this.children) == this.max_children:
			this.message(target, 'I\'m sorry ' + user + ', these hips just can\'t handle no more...')

	def update_child_bearing(this):
		this.isAbleToBear = True
		this.childTimer.cancel()

	def remove_child(this, child_pos):
		dead_child = this.children.pop(child_pos)
		dead_socket = this.sockets.pop(child_pos + 1)
		dead_socket.shutdown(socket.SHUT_RDWR)
		dead_socket.close()

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
			child_count = 0
			for child in this.children:
				if child.isAlive == False:
					this.remove_child(child_count)
				if(child.sock in ready_to_read and child.isAlive):
					line2 = child.sock.recv(500)
					if len(line2) > 0:
						print 'Child --- ' + child.NICK + '::' + line2
					child.handle_message(line2)
				child_count += 1