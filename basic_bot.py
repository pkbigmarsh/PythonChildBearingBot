import sys
import socket
import string
import os

class BasicBot():
	def __init__(this, host, nick, owner, channel_list):
		this.HOST = host
		this.NICK = nick
		this.IDENT = nick
		this.REALNAME = nick
		this.CHANNEL_LIST = channel_list
		this.PORT = 6667
		this.OWNER = owner
		this.sock = socket.socket()

	def connect(this):
		this.sock.connect((this.HOST, this.PORT))
		this.sock.send('NICK ' + this.NICK + '\n')
		this.sock.send('USER ' + this.IDENT + ' ' + this.HOST + ' bla :' + this.REALNAME + '\n')

	def message(this, target, msg):
		this.sock.send('PRIVMSG ' + target + " :" + msg + '\n')

	def join(this, channel):
		print 'Joining: ' + channel
		this.sock.send('JOIN ' + channel + '\n')

	def parseUser(this, msg):
		user_end_pos = msg.find('!');
		user_begin_pos = msg[:user_end_pos].find(':') + 1
		if user_begin_pos == 0:
			return 'User not found'
		return msg[user_begin_pos:user_end_pos]

	def parsePRIVMSG(this, msg):
		command_pos = msg.find('PRIVMSG')
		if(command_pos == -1):
			return 'Command not found'
		msg = msg[command_pos:]
		msg_pos = msg.find(':')
		target = msg[:msg_pos]
		message = msg[msg_pos + 1:]
		target = msg.split()[1]
		return target, message


	def parsemsg(this, msg):
		sender_nick = this.parseUser(msg)
		sender, message = this.parsePRIVMSG(msg)
		print '\n\n'
		print 'The sender is ' + sender_nick
		print 'From sender: ' + sender
		print 'With the message of:' + message

	def pingPong(this, msg):
		msg = msg.rstrip()
		msg = msg.split()
		this.sock.send("PONG "+msg[1]+"\n")

	def basic_message_handle(this, msg):
		if msg.find("Welcome") != -1:
			this.join(this.CHANNEL_LIST)
		elif msg.find("PRIVMSG") != -1:
			this.parsemsg(msg)
		elif msg.find('PING') != -1:
			this.pingPong(msg)

	def run(this):
		this.sock.connect((this.HOST, this.PORT))
		this.sock.send('NICK ' + this.NICK + '\n')
		this.sock.send('USER ' + this.IDENT + ' ' + this.HOST + ' bla :' + this.REALNAME + '\n')

		while 1:
			line = this.sock.recv(500)
			if len(line) > 0:
				print line
			this.basic_message_handle(line)