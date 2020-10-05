from random import random
from colorama import Fore
from lines import *
import msvcrt
from enum import Enum
from string import ascii_lowercase # can expand later but for now a..z for inventory

class Item_Type(Enum): # don't think will be used
	WEAPON = 0 # etc.
	ARMOR = 1

class Player:
	def __init__(self, name, symbol, xp, level):
		# NOTE can make init contain level, so fits within map...
		self.name = name
		self.symbol = symbol
		self.x = 1
		self.y = 1
		place_start_player(self, level)
		
		self.xp = xp
		self.level = 1
		self.hp = 20 * self.level
		self.max_hp = 20 * self.level
		self.inventory = {} # shold make this a dictionary of letters/nums to items
		self.equipped_items = {} # can make dictionary entries "head", etc. ? or still letters probably...
		# might not use above
		self.weapon = None # expand to left right later
		self.armor = None

	def get_item(self, item):
		position = "a"
		while self.inventory.get("a") != None:
			pass
		for pos in ascii_lowercase:
			if self.inventory.get(pos) != None:
				# letter/slot already used
				pass
			else:
				# add to inventory
				self.inventory[pos] = item
				return
		# no space present if exit loop
		print("No space in inventory.")
		
	def advance_level(self):
		if self.xp >= 20*self.level: # TODO set this scaling
			# advance a level
			self.level += 1
			if self.hp + 5 * self.level:
				 self.hp += 5 * self.level
			self.max_hp = 20 * self.level

	def kill(self, entity, level):
		# kills an entity on this level, dropping their loot and bones where they stood,
		# and yielding it to player
		for item in entity.inventory:
			# drop all items
			level.items[entity.y][entity.x].append(item)
		print(entity.xp)
		self.xp += entity.xp # gain xp of fallen foe
		print(entity.name, " has been slain.")
		# note del doesn't work well since referenced multiple places, rather remove from entities?
		# *should* only have 2 refs so perhaps can delete after removing entities
		level.entities[entity.y][entity.x] = None
		del entity # remove enemy object
		# killing gains xp so only check for level up here
		self.advance_level()

	def attack(self, entity, level):
		# damages entity, TODO add ac
		if self.weapon == None:
			damage = 1 # default hit damage
		else:
			damage = self.weapon.damage # must make sure hand hold weapon (i.e. no gloves) --- swap to "weapon" and "shield" etc, come up with some other way to have 2 handed maybe
		entity.hp -= damage
		# check if entity dead or do elsewhere?
		if entity.hp <= 0:
			self.kill(entity, level)

class Item:
	def __init__(self, name, symbol):
		self.name = name
		self.symbol = symbol
		#self.item_type = item_type

class Weapon(Item):
	# instead of Enum make subclasses, equip method for each
	def __init__(self, name, damage):
		super().__init__(name, "w") # if subclasses e.g. sword axe can further differentiate
		self.damage = damage

	def equip(self, player):
		player.weapon = self

class Armor(Item):
	def __init__(self, name, ac):
		super().__init__(name, "a")
		self.ac = ac

	def equip(self, player):
		player.armor = self

class Level:
	# hold tiles, enemies, and items?
	def __init__(self):
		# TODO flush out enemy generation
		# need functions to generate them
		self.size = 50
		# need tiles to be a tile class or something
		# for now using 0=empty 1=wall
		self.tiles = [[1 for i in range(self.size)] for i in range(self.size)]
		for i in range(self.size):
			# setting up some basic walls around edge
			self.tiles[0][i] = 1
			self.tiles[i][0] = 1
			self.tiles[self.size-1][i] = 1
			self.tiles[i][self.size-1] = 1
		self.generate_floor()
		# need monsters to be own class, make same as player class?
		self.entities = [[None for i in range(self.size)] for i in range(self.size)] #[] #[[None for i in range(self.size)] for i in range(self.size)] # monsters array since only 1 per spot max... but need then special funcs to move monsters so will do one single list
		#self.monsters.append(Player("orc", "o", 10, self))
		for i in range(10):
			orc = Player("orc", "o", 10, self)
		#place_item(orc, self)

		# should above be an array or list? probably list since will be players, have x,y
		# only problem is slower, have to check each list entry see if xy matches...
		# since monsters can't stack maybe better to do array, but for items do list since can stack? or make list at each point actually
		self.items = [[[] for i in range(self.size)] for i in range(self.size)]

	def generate_room(self, count):
		# NOTE count is # tries take, after some number give up...
		if count > 10:
			return (-1,-1) # i.e. failure
		# procedure: pick point to be middle, ensure does not hit walls or other rooms, then clear out
		# first, pick center somewhere within int([0.0,1.0)*size) = 0,1,...,size-2,size-1 (perfect for array addressing?)
		center_y = int(random()*self.size)
		center_x = int(random()*self.size) 
		# now pick size of room
		widthy = int(random()*11) + 1 # can tweak, for now somewhere in 1,2,3,...,12 tiles to a side free (+ 1 for center)
		widthx = int(random()*11) + 1
		# then, ensure does not pass edges (i.e. center +- width within bounds) and not breaching another room(? not *necessary*) (i.e. no tiles already free... assuming we start with a completely wall filled floor plan)
		# need to give 1 tile berth of edge so walled off
		# check edges:
		if center_y - widthy < 1 or center_y + widthy > self.size-2 or center_x - widthx < 1 or center_x + widthx > self.size-2:
			(x,y) = self.generate_room(count + 1) # i.e. try again
			return (x,y) # complete
		# check other rooms: (will have to come up with how to connect rooms next... maybe could return the center position?)
		for y in range(center_y - widthy, center_y + widthy + 1):
			for x in range(center_x - widthx, center_x + widthx + 1):
				if not self.tiles[y][x]:
					# i.e. room already taken
					(x,y) = self.generate_room(count + 1)
					return (x,y)
		# passed checks, ok to return after clearing
		for y in range(center_y - widthy, center_y + widthy + 1, 1):
			for x in range(center_x - widthx, center_x + widthx + 1, 1):
				self.tiles[y][x] = 0
				#print(":!")
				#self.tiles[center_y][center_x] = -1		
		return (center_x,center_y)

	def generate_hallway(self, centerx1, centery1, centerx2, centery2):
		plot_line(centerx1, centery1, centerx2, centery2, self.tiles, 0)

	def generate_floor(self):
		# generate a number of floors or until unable to generate (i.e. (-1,-1))
		# then connect rooms
		max_floors = 10
		rooms = [] # list of centers
		# gen. rooms
		for i in range(max_floors):
			room = self.generate_room(0)
			if room == (-1,-1):
				break # goto hall filling
			rooms.append(room)
		# gen. halls
		for i in range(0, len(rooms) - 1, 1):
			(x1pos, y1pos) = rooms[i]
			(x2pos, y2pos) = rooms[i+1]

			self.generate_hallway(x1pos, y1pos, x2pos, y2pos)
		return


def main():
	#global turncount
	#turncount = 0
	level = Level() # will make a list of levels later
	player = Player("Alex", "@", 0, level)
	time = Time()
	#orc = Player("orc", "o", 10)
	#player.inventory["a"] = Weapon("Sword", 10) # need func to do this automatically
	player.get_item(Weapon("Sword", 10))
	
	#place_start_player(player, level)
	tilegraphics = generate_graphics()
	display(player, level, tilegraphics, time)
	while process_input(player, level):
		time.time_update(player, level)
		#print(player.x, player.y)
		display(player, level, tilegraphics, time)

		#turncount += 1
	return

class Time:

	heal_rate = 0.1

	def __init__(self):
		self.heal_time = 0
		self.turncount = 0 # ???
	
	def time_update(self, player, level):
		self.turncount += 1
		self.heal_time += 1
		if int(self.heal_rate*self.heal_time) >= 1:
			if player.hp < player.max_hp:
				player.hp += 1
			self.heal_time = 0


# def time_update(player, level):
# 	# heal and other things that happen over time
# 	heal_rate = 0.1 # need saved outside?
# 	if (heal_rate*turncount) >= 1:
# 		# eligible for healing


def calculate_LoS(entity, level):
	# use line func above, modified so *checks* each tile, then if wall, stop
	# looking past that, add visible tiles to set and output
	# start with 8x8 grid like dcss, look to each point on boundary
	visible = [] # set of visible points (perhaps duplicates?)
	ex = entity.x
	ey = entity.y
	boundary = [(ex+4,ey+4),(ex+4,ey+3),(ex+4,ey+2),(ex+4,ey+1),(ex+4,ey),(ex+4,ey-1),(ex+4,ey-2),(ex+4,ey-3),(ex+4,ey-4),
				(ex-4,ey+4),(ex-4,ey+3),(ex-4,ey+2),(ex-4,ey+1),(ex-4,ey),(ex-4,ey-1),(ex-4,ey-2),(ex-4,ey-3),(ex-4,ey-4),
				(ex-4,ey+4),(ex-3,ey+4),(ex-2,ey+4),(ex-1,ey+4),(ex,ey+4),(ex+1,ey+4),(ex+2,ey+4),(ex+3,ey+4),(ex+4,ey+4),
				(ex-4,ey-4),(ex-3,ey-4),(ex-2,ey-4),(ex-1,ey-4),(ex,ey-4),(ex+1,ey-4),(ex+2,ey-4),(ex+3,ey-4),(ex+4,ey-4)]
	# for bx,by in boundary:
	# 	# apply line func, stop when hit wall, return hit set of points
	# 	visible += los_line(ex, ey, bx, by, level.tiles)
	for x in range(-4, 5, 1):
		for y in range(-4, 5, 1):
			# will have to ensure doesn't look out of bounds :(
			if x != 0 or y != 0:
				visible += los_line(ex, ey, ex+x, ey+y, level.tiles)
	return visible

def place_start_player(player, level):
	# finds a good spot to put player
	xpos = int(random()*level.size)
	ypos = int(random()*level.size)
	while int(level.tiles[ypos][xpos]) or level.entities[ypos][xpos] != None:
		xpos = int(random()*level.size)
		ypos = int(random()*level.size)
	player.x = xpos
	player.y = ypos
	level.entities[ypos][xpos] = player
	#return (xpos, ypos)

def place_item(item, level):
	# finds a good spot to put item
	xpos = int(random()*level.size)
	ypos = int(random()*level.size)
	while int(level.tiles[ypos][xpos]):
		xpos = int(random()*level.size)
		ypos = int(random()*level.size)
	level.items[ypos][xpos].append(item)

def move(entity, x, y, level):
	# NOTE could place monster on map array so quick, but then moving complicated and separate from player... instead
	# could have monsters in list but have to check each element :( ...
	# could do both, store in array and keep x,y ? faster but kinda complicated
	# think I will do array option -> i.e. level has monsters[][], keep matched with monster.x,y
	# can return false if unable to complete?
	if level.tiles[entity.y + y][entity.x + x] == 1:
		return False
	if level.entities[entity.y + y][entity.x + x] != None:
		entity.attack(level.entities[entity.y + y][entity.x + x], level)
		return True
	level.entities[entity.y][entity.x] = None
	entity.x += x
	entity.y += y
	level.entities[entity.y][entity.x] = entity
	# need to update entities grid too

	return True

def process_input(player, level):
	# TODO need a way to have commands that pass a turn and those that don't e.g. inventory (or have all inventory actions contained within e.g. "i" maybe)
	# add handling if move can't complete etc.
	#inpt = input(">")
	inpt = (msvcrt.getch()).decode('utf-8') # windows dependent
	if inpt == "j": # down
		move(player, 0, -1, level)
	elif inpt == "k": # up
		move(player, 0, 1, level)
	elif inpt == "h": # left
		move(player, -1, 0, level)
	elif inpt == "l": # right
		move(player, 1, 0, level)
	elif inpt == "n": # SE
		move(player, 1, -1, level)
	elif inpt == "b": # SW
		move(player, -1, -1, level)
	elif inpt == "y": # NW
		move(player, -1, 1, level)
	elif inpt == "u": # NW
		move(player, 1, 1, level)
	elif inpt == "i": # inventory
		access_inventory(player, level) # maybe make this redo function so doesn't pass turn? idk
	elif inpt == "g": # get
		pickup_item(player, level)
	elif inpt == "e": # equip
		equip_item(player)
	elif inpt == "d": # drop
		drop_item(player, level)
	elif inpt == "q":
		return False
	else:
		print(inpt, " is not a recognized command")
		return process_input(player, level)
	return True

def generate_graphics():
	# TODO rather, record the ascii within each class? i.e. player, item, etc?
	# records the ascii to be used for different items
	# we can keep for walls/floors?
	tiles_dictionary = {}
	tiles_dictionary["floor_empty"] = "."
	tiles_dictionary["wall"] = "#"
	tiles_dictionary["player"] = "@"
	tiles_dictionary["sword"] = "s"
	return tiles_dictionary

def display_inventory(player):
	print("--- Inventory ---")
	for (letter, item) in player.inventory.items():
		print(letter, " - ", item.name)
	# now print equipment slots
	print("--- Equipment ---")
	if player.weapon != None:
		print("weapon - ", player.weapon.name)
	else:
		print("weapon - empty")

def equip_item(player):
	print("Equip which item?")
	inpt = (msvcrt.getch()).decode('utf-8')
	item = player.inventory.get(inpt)
	while item == None:
		print("No such item.")
		inpt = (msvcrt.getch()).decode('utf-8')
		item = player.inventory.get(inpt)
	#if player.equipped_items.get(inpt)
	#player.equipped_items[inpt] = item
	#item_type = item.
	item.equip(player)
	print("ok")

def drop_item(player, level):
	# probably have level store list of items, each stores its x,y but what about when in inventory??? set xy none?
	print("which item to drop?")
	inpt = (msvcrt.getch()).decode('utf-8')
	item = player.inventory.get(inpt)
	while item == None:
		print("No such item.")
		inpt = (msvcrt.getch()).decode('utf-8')
		item = player.inventory.get(inpt)

	level.items[player.y][player.x].append(item)
	# remove item from dictionary:
	player.inventory = {key:value for k,v in player.inventory.items() if v != item}
	#del player.inventory[itemkey] # TODO ensure del works... need key
	# next check every equipment slot
	if player.weapon == item:
		player.weapon = None
		# etc.
		# should item have location or level store it?

def pickup_item(player, level):
	# TODO for simplicity begin with taking last element, expand to selection screen later
	# need method to add to inventory, separate from this (should it be func of player class? yes since doesn't need level just item)
	if not level.items[player.y][player.x]:
		print("No items here.")
		return
	item = level.items[player.y][player.x].pop() # remove last element from list
	player.get_item(item)


def process_input_inventory(player, level): # don't do this... need letters to access items, and should be able to equip even not looking at inventory
	inpt = (msvcrt.getch()).decode('utf-8')
	if inpt == "q":
		return False
	# elif inpt == "e": # equip
	# 	equip_item(player)
	# elif inpt == "d": # drop
	# 	drop_item(player, level)
	# elif inpt == "g": # get
	# 	pickup_item(player, level)
	else:
		print(inpt, " is not a recognized command")
		return process_input(player, level)
	return True

def access_inventory(player, level):
	display_inventory(player)
	while process_input_inventory(player, level):
		display_inventory(player)
		#pass


def display(player, level, tilegraphics, time):
	# again inefficient defined each time, make lookup file/dictionary?
	los = calculate_LoS(player, level)

	for y in range(level.size-1, -1, -1):
		print("")
		for x in range(level.size):
			if (x,y) in los:
				print(Fore.WHITE + "", end = "")
			else:
				print(Fore.BLUE + "", end = "")
			# if y == player.y and x == player.x:
			# 	#print(tilegraphics.get("player"), end='') # not efficient but whatever for now
			# 	print(player.symbol, end='')
			if level.entities[y][x] != None:
				print(level.entities[y][x].symbol, end="")
			# elif (x,y) in los:
			# 	print(Fore.RED + "x", end='')
			else:
				if level.items[y][x]: # if items present, print top item
				 	print(level.items[y][x][-1].symbol, end='')
				elif level.tiles[y][x] == 0:
					print(tilegraphics.get("floor_empty"), end='')
				# elif level.tiles[y][x] == -1:
				# 	print("x", end='')
				else:
					print(tilegraphics.get("wall"), end='')
	print(Fore.WHITE + "\n", end = "")
	print("Name: ", player.name, " HP: ", player.hp, "/", player.max_hp, " XP: ", player.xp, " Lvl: ", player.level, " Time: ", time.turncount)

turncount = 0
main()