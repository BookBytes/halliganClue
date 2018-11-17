import random
import itertools

def Card(Object):
	def __init__ (self, name, card_img):
		self.name = name
		self.image = card_img
def Deck(Object):
	def __init__ (self):
		characters = ['Donna “The Coordinator” Cerelli',\
		'Mark "The Shark" Sheldon',\
		'Megan “The Administrator” Monaghan ',\
		'Megan "The Captain" Monroe ',\
		'Ming “The Hacker” Chow',\
		'Norman “The Linguist” Ramsey']
		items = ['NP = P proof', '105 Textbook',\
		'SQL Injection','Binary Bomb','Dead squirrel',\
		'Dry white board marker']
		places = ['Collab Room','Entry way','EECS Office',\
		'Kitchen','Fishbowl','The Computer Lab','Couches',\
		'Admin Office','Extension']
		char = random.choice(characters)
		item = random.choice(items)
		place = random.choice(places)
		self.solution = [char,item,place]
		characters.remove(char)
		items.remove(item)
		places.remove(place)
		first = itertools.chain(characters,items)
		all_place = itertools.chain(first, places)



def Game(object):

