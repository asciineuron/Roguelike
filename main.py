from random import random
from colorama import Fore
from lines import *
import msvcrt

class Player:
	def __init__(self, name):
		self.name = name
		self.x = 1
		self.y = 1
		self.xp = 0
		self.items = []

class Level:
	# hold tiles, enemies, and items?
	def __init__(self):
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
		self.monsters = [[0 for i in range(self.size)] for i in range(self.size)]

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

		# # TODO still doesn't always work....
		# # open all tiles between the two centers
		# dx = centerx2-centerx1
		# dy = centery2-centery1
		# #if dy%dx != 0:
		# 	# i.e. want even number of y steps per x step for clearing
		# 	# pick dy or dx to increase?
		# 	# perhaps we could just estimate and do int division, have some error by end
		# y = centery1
		# x = centerx1
		# if dx != 0:
		# 	dydx = int(dy/dx)
		# 	for x in range(centerx1, centerx2, int(dx/abs(dx))): # NOTE might have to fix sign of + 1 if centerx2 < centerx1...
		# 		if dydx != 0:
		# 			for i in range(0, dydx , int(dydx/abs(dydx))): # had dydx + int(dydx/abs(dydx))
		# 				y += int(dy/abs(dy))
		# 				#print(dydx, y)
		# 				self.tiles[y][x] = 0
		# 		else:
		# 			# i.e. only x steps
		# 			self.tiles[y][x] = 0
		# else:
		# 	# i.e. only y steps, NOTE for now assuming dy can't be 0 too... would be same spot
		# 	for y in range(centery1, centery2, int(dy/abs(dy))):
		# 		self.tiles[y][x] == 0


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
	player = Player("Alex")
	level = Level() # will make a list of levels later
	place_start_player(player, level)
	tilegraphics = generate_graphics()
	display(player, level, tilegraphics)
	while process_input(player, level):
		#print(player.x, player.y)
		display(player, level, tilegraphics)

	return



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
	while int(level.tiles[ypos][xpos]):
		xpos = int(random()*level.size)
		ypos = int(random()*level.size)
	player.x = xpos
	player.y = ypos


def move(entity, x, y, level):
	# can return false if unable to complete?
	if level.tiles[entity.y + y][entity.x + x] == 1:
		return False
	entity.x += x
	entity.y += y
	return True

def process_input(player, level):
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
	elif inpt == "q":
		return False
	else:
		print(inpt, " is not a recognized command")
		return process_input(player, level)
	return True

def generate_graphics():
	# records the ascii to be used for different items
	tiles_dictionary = {}
	tiles_dictionary["floor_empty"] = "."
	tiles_dictionary["wall"] = "#"
	tiles_dictionary["player"] = "@"
	return tiles_dictionary

def display(player, level, tilegraphics):
	# again inefficient defined each time, make lookup file/dictionary?
	los = calculate_LoS(player, level)

	for y in range(level.size-1, -1, -1):
		print("")
		for x in range(level.size):
			if (x,y) in los:
				print(Fore.WHITE + "", end = "")
			else:
				print(Fore.BLACK + "", end = "")
			if y == player.y and x == player.x:
				print(tilegraphics.get("player"), end='') # not efficient but whatever for now
			# elif (x,y) in los:
			# 	print(Fore.RED + "x", end='')
			else:
				if level.tiles[y][x] == 0:
					print(tilegraphics.get("floor_empty"), end='')
				# elif level.tiles[y][x] == -1:
				# 	print("x", end='')
				else:
					print(tilegraphics.get("wall"), end='')
	print(Fore.WHITE + "\n", end = "")
	print("Name: ", player.name, " XP: ", player.xp)


main()