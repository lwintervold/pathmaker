import pygame
import heapq
import math

from typing import Tuple
from typing import List
from typing import Set

dimension = 800
screen = pygame.display.set_mode((dimension, dimension))
padding = 1
cellsize = 10

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

def euclidianDistance(
	start : Tuple[int, int],
	end : Tuple[int, int]
	) -> int:

	(sx, sy) = start
	(ex, ey) = end
	return math.sqrt((sx - ex) ** 2 + (sy - ey) ** 2)

def getNeighbors(
	coords : Tuple[int, int],
	blocked : Set[Tuple[int, int]],
	bounds : Tuple[int, int]
	) -> List[Tuple[int, int]]:

	neighbors = []
	(x, y) = coords
	(boundx, boundy) = bounds
	for ix in range(x - 1, x + 2):
		for iy in range(y - 1, y + 2):
			# Check self
			if ix == x and iy == y:
				continue

			# Check bounds
			if ix < 0 or iy < 0 or ix >= boundx or iy >= boundy:
				continue

			# Check blocked
			if (ix, iy) in blocked:
				continue

			neighbors.append((ix, iy))
	return neighbors

def aStarPath(
	start : Tuple[int, int],
	end : Tuple[int, int],
	blocked : Set[Tuple[int, int]],
	bounds : Tuple[int, int]
	) -> List[Tuple[int, int]]:

	frontier = [(0, start)]
	originpaths = {}
	costs = {}
	costs[start] = 0

	while len(frontier) > 0:
		current = heapq.heappop(frontier)[1]
		
		if current == end:
			path = []
			while current in originpaths:
				path.append(current)
				current = originpaths[current]
			return path

		neighbors = getNeighbors(current, blocked, bounds)
		for neighbor in neighbors:
			new_cost = costs[current] + euclidianDistance(current, neighbor)
			if neighbor not in costs or new_cost < costs[neighbor]:
				# This is a better path
				originpaths[neighbor] = current
				costs[neighbor] = new_cost
				combined_cost = new_cost + euclidianDistance(neighbor, end)
				heapq.heappush(frontier, (combined_cost, neighbor))
	return None

def drawRectFromNormCoords(
	coords : Tuple[int, int],
	color : Tuple[int, int, int]
	) -> None:

	(x, y) = coords
	rx = x * cellsize + padding
	ry = y * cellsize + padding
	pygame.draw.rect(
		screen,
		color,
		pygame.Rect(rx, ry, cellsize - padding, cellsize - padding))

def mouseCoordsToNormCoords(
	mcoords : Tuple[int, int]
	) -> Tuple[int, int]:

	(mx, my) = mcoords
	x = (mx - padding) // cellsize
	y = (my - padding) // cellsize
	return (x, y)

def clearDrawnPath(
	path : List[Tuple[int, int]],
	blocked_coords : Set[Tuple[int, int]]
	) -> None:
	for coords in path:
		if coords not in blocked_coords:
			drawRectFromNormCoords(coords, WHITE)

if __name__ == '__main__':
	for row in range(dimension // cellsize):
		for col in range(dimension // cellsize):
			pygame.draw.rect(screen,
				WHITE,
				pygame.Rect(col * cellsize + padding,
				 row * cellsize + padding,
				 cellsize - padding,
				 cellsize - padding))
	pygame.display.update()
	blocked_coords = set()
	alive = True
	path = None
	while alive:
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				newpath = aStarPath((5,5), (70, 70), blocked_coords, (dimension // cellsize, dimension // cellsize))
				if newpath is None:
					continue
				if path is not None:
					# Clear old path
					clearDrawnPath(path, blocked_coords)
				for coords in newpath:
					drawRectFromNormCoords(coords, GREEN)
				path = newpath
				pygame.display.update()

			if pygame.mouse.get_pressed()[0]:
				coords = mouseCoordsToNormCoords(pygame.mouse.get_pos())
				if pygame.key.get_mods() & pygame.KMOD_SHIFT:
					color = WHITE
					blocked_coords.discard(coords)
				else:
					color = BLACK
					blocked_coords.add(coords)
				
				drawRectFromNormCoords(coords, color)
				pygame.display.update()