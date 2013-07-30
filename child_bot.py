from basic_bot import *
from threading import Timer
import random
import re

class ChildBot(BasicBot):
	def __init__(this, host, nick, channel, mother):
		BasicBot.__init__(this, host, nick, channel)
		this.heartbeat = Timer(5, this.beat_heart)
		this.heartbeat.start()
		this.hunger = 0
		this.thirst = 0
		this.love = 0
		this.max_ignore = 3
		this.mother_nick = mother
		this.isAlive = True
		random.seed()

	def beat_heart(this):
		print this.NICK + ' - heartbeat'
		choice = random.randint(0,2)
		if choice == 0:
			this.hunger += 1
		elif choice == 1:
			this.thirst += 1
		elif choice == 2:
			this.love += 1

		if this.hunger > this.max_ignore:
			this.death_by_hunger()
		elif this.thirst > this.max_ignore:
			this.death_by_thirst()
		elif this.love > this.max_ignore:
			this.death_by_love()
		else:
			if this.hunger > this.thirst and this.hunger > this.love:
				this.hunger_message()
			elif this.thirst > this.hunger and this.thirst > this.love:
				this.thirst_message()
			elif this.love > this.hunger and this.love > this.thirst:
				this.love_message()
			else:
				this.random_message()
		this.heartbeat = Timer(5, this.beat_heart)
		this.heartbeat.start()

	def random_message(this):
		choice = random.randint(0,2)
		print('random message: ', choice)
		if choice == 0:
			this.thirst_message()
		elif choice == 1:
			this.love_message()
		elif choice == 2:
			this.hunger_message()

	def death_by_hunger(this):
		this.message(this.CHANNEL_LIST, 'Moommmmmmyyyyy I hungyyyy... bye... bye...')
		this.disconnect()

	def death_by_thirst(this):
		this.message(this.CHANNEL_LIST, 'I\'m soooo thirsty... bye... bye...')
		this.disconnect()

	def death_by_love(this):
		this.message(this.CHANNEL_LIST, 'I guess I might as well run away... Mommy doesn\'t even notice me...')
		this.disconnect()

	def hunger_message(this):
		choice = random.randint(0,2)
		print('Hunger message: ', choice)
		if choice == 0:
			this.message(this.CHANNEL_LIST, 'Is there any food')
		elif choice == 1:
			this.message(this.CHANNEL_LIST, 'I\'m sooooo hungry... ' + this.mother_nick + ' can I have a snack?')
		elif choice == 2:
			this.message(this.CHANNEL_LIST, 'Feed me mommy!!')

	def thirst_message(this):
		choice = random.randint(0, 2)
		print('Thirst message: ', choice)
		if choice == 0:
			this.message(this.CHANNEL_LIST, 'Is there any drink?')
		elif choice == 1:
			this.message(this.CHANNEL_LIST, 'I\'m sooooo thirsy... ' + this.mother_nick + ' can I have a soda? pwease? pwease??')
		elif choice == 2:
			this.message(this.CHANNEL_LIST, 'I want a mountain dew!!!')

	def love_message(this):
		choice = random.randint(0, 2)
		print('Love message: ', choice)
		if choice == 0:
			this.message(this.CHANNEL_LIST, 'Do you love me?')
		elif choice == 1:
			this.message(this.CHANNEL_LIST, 'Can I have a hug?')
		elif choice == 2:
			this.message(this.CHANNEL_LIST, 'Love me mommy...')

	def disconnect(this):
		this.sock.close()
		this.heartbeat.cancel()
		this.isAlive = False

	def parse(this, msg):
		user = this.parseUser(msg)
		target, message = this.parsePRIVMSG(msg)

		food_rgexp = '(food|snack|steak|chips)'
		thirst_rgexp = '(drink|soda|mtn dew|mountain dew|water|coffee|tea)'
		love_rgexp = '(love|hug|high five|' + this.NICK + ')'

		if user == this.mother_nick:
			# Search for food action
			search = re.compile(food_rgexp, re.I)
			results = re.search(search, message)
			if results and this.hunger > 0:
				this.message(this.CHANNEL_LIST, 'Mommy fed me!! :)')
				this.hunger -= 1

			# Search for thirst action
			search = re.compile(thirst_rgexp, re.I)
			results = re.search(search, message)
			if results and this.thirst > 0:
				this.message(this.CHANNEL_LIST, 'I\'m not so thirsy any more mommy :)')
				this.thirst -= 1

			# Search for love action
			search = re.compile(love_rgexp, re.I)
			results = re.search(search, message)
			if results and this.love > 0:
				this.message(this.CHANNEL_LIST, 'I love you too mommy :)')
				this.love -= 1

	def handle_message(this, msg):
		if len(msg) > 0:
			print 'Child --- ' + this.NICK + '::' + msg
		if msg.find("Welcome") != -1:
			this.join(this.CHANNEL_LIST)
			this.message(this.CHANNEL_LIST, this.mother_nick + ', hi mommy!!!! :)')
		elif msg.find("PRIVMSG") != -1:
			this.parse(msg)
		elif msg.find('PING') != -1:
			this.pingPong(msg)