import sys
import socket
import string
import os

class bot_child():
	def __init__(this, host, nick, ident, realname, channel):
		this.HOST = host
		this.NICK = nick
		this.IDENT = ident
		this.REALNAME = realname
		this.CHANNEL_LIST = channel
		this.PORT = 6667
		this.OWNER = 'msumwalt'
		this.sock = socket.socket()

	def message(this, target, msg):
		this.sock.send('PRIVMSG ' + target + " :" + msg + '\n')

	def join(this, channel):
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
		if message.find('PythonBot2000') != -1 and sender_nick != 'InternBot':
			response = "Hello " + sender_nick + '!! You are kind, ' + sender_nick + '++'
			this.message(sender, response)
		if message.find('Create bot ') != -1:
			cmd = 'Create bot '
			bot_name = message[message.find(cmd) + len(cmd):].split()[0]
			this.message(sender, 'New Bot: ' + bot_name)

	def pingPong(this, msg):
		msg = msg.rstrip()
		msg = msg.split()
		this.sock.send("PONG "+msg[1]+"\n")

	def run(this):
		this.sock.connect((this.HOST, this.PORT))
		this.sock.send('NICK ' + this.NICK + '\n')
		this.sock.send('USER ' + this.IDENT + ' ' + this.HOST + ' bla :' + this.REALNAME + '\n')

		while 1:
			line = this.sock.recv(500)
			if len(line) > 0:
				print line
			if line.find("Welcome to the Lexmark-Lpdev") != -1:
				this.join(this.CHANNEL_LIST)
			elif line.find("PRIVMSG") != -1:
				this.parsemsg(line)
			elif line.find('PING') != -1:
				this.pingPong(line)