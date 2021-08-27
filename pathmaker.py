import pygame # type: ignore
import heapq
import math
import matplotlib.pyplot as plt

from typing import Tuple
from typing import List
from typing import Set
from typing import Optional
from typing import Dict

dimension = 800
screen = pygame.display.set_mode((dimension, dimension))
padding = 1
cellsize = 10

COLORMAX = 255
COLORINTERVAL = 64

WHITE = (COLORMAX, COLORMAX, COLORMAX)
GREEN = (0, COLORMAX, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, COLORMAX)
RED = (COLORMAX, 0, 0)

def normalizeColor(
  color : Tuple[int, int, int]
  ) -> Tuple [float, float, float]:

    return tuple(map(lambda x: x / 255 if x != 0 else 0, color))

def heightToColor(
  height : int
  ) -> int:

  scale = min(abs(height) * COLORINTERVAL, COLORMAX)
  if height < 0:
    sub = (scale, scale, 0)
  else:
    sub = (0, scale, scale)
  return tuple(map(lambda x, y : x - y, WHITE, sub))

def euclidianDistance(
  start : Tuple[int, int],
  end : Tuple[int, int],
  heights : Dict[Tuple[int, int], int]
  ) -> float:

  (sx, sy) = start
  (ex, ey) = end
  sz = heights[start] if start in heights else 0
  ez = heights[end] if end in heights else 0
  return math.sqrt((sx - ex) ** 2 + (sy - ey) ** 2 + (sz - ez) ** 2)

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
  bounds : Tuple[int, int],
  heights : Dict[Tuple[int, int], int]
  ) -> Optional[List[Tuple[int, int]]]:

  frontier : List[Tuple[float, Tuple[int, int]]] = [(0, start)]
  originpaths: Dict[Tuple[int, int], Tuple[int, int]] = {}
  costs: Dict[Tuple[int, int], float] = {}
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
      new_cost = costs[current] + euclidianDistance(current, neighbor, heights)
      if neighbor not in costs or new_cost < costs[neighbor]:
        # This is a better path
        originpaths[neighbor] = current
        costs[neighbor] = new_cost
        combined_cost = new_cost + euclidianDistance(neighbor, end, heights)
        heapq.heappush(frontier, (combined_cost, neighbor))
  return []

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
  blocked_coords : Set[Tuple[int, int]],
  heights : Dict[Tuple[int, int], int]
  ) -> None:
  for coords in path:
    if coords not in blocked_coords:
      color = heightToColor(heights[coords]) if coords in heights else WHITE
      drawRectFromNormCoords(coords, color)

if __name__ == '__main__':
  heights : Dict[Tuple[int, int], int] = {}
  for row in range(dimension // cellsize):
    for col in range(dimension // cellsize):
      heights[(row, col)] = 0
      pygame.draw.rect(screen,
        WHITE,
        pygame.Rect(col * cellsize + padding,
         row * cellsize + padding,
         cellsize - padding,
         cellsize - padding))
  pygame.display.update()
  blocked_coords: Set[Tuple[int, int]] = set()
  heights: Dict[Tuple[int, int], float] = {}
  path = []
  while True:
    for event in pygame.event.get():

      if event.type == pygame.QUIT:
        pygame.quit()
        exit()

      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        newpath = aStarPath((5,5), (70, 70), blocked_coords, (dimension // cellsize, dimension // cellsize), heights)
        if len(newpath) == 0:
          continue
        if len(path) > 0:
          # Clear old path
          clearDrawnPath(path, blocked_coords, heights)
        for coords in newpath:
          drawRectFromNormCoords(coords, GREEN)
        path = newpath
        pygame.display.update()

      if event.type == pygame.KEYDOWN  and event.key == pygame.K_3:
        n_green = normalizeColor(GREEN)
        n_blue = normalizeColor(BLUE)
        n_clear = (0, 0, 0, 0)
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(121, projection='3d')
        _x = [x for x in range(dimension // cellsize) for y in range(dimension // cellsize)]
        _y = [y for x in range(dimension // cellsize) for y in range(dimension // cellsize)]
        _h = [heights[height] if height in heights else 0 for height in zip(_x, _y)]
        _c = [n_green if coords in path else n_clear if coords in blocked_coords else n_blue for coords in zip(_x, _y)]
        ax._autoscaleZon = False
        ax.set_zbound( -math.ceil(COLORMAX / COLORINTERVAL) * 2, math.ceil(COLORMAX / COLORINTERVAL) * 2)
        ax.bar3d(_x, _y, 0, 1, 1, _h, color= _c)
        ax.view_init(60, 100)
        ax.invert_yaxis()
        plt.tight_layout()
        plt.axis('off')
        plt.show()

      pressed = pygame.mouse.get_pressed()
      coords = mouseCoordsToNormCoords(pygame.mouse.get_pos())
      if pressed[0]:
        heights[coords] = 0
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
          color = WHITE
          blocked_coords.discard(coords)
        else:
          color = BLACK
          blocked_coords.add(coords)
        drawRectFromNormCoords(coords, color)
        pygame.display.update()
      if pressed[2]:
        if coords in blocked_coords:
          continue
        height = heights[coords] if coords in heights else 0
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
          height = max(height - 1, -math.ceil(COLORMAX / COLORINTERVAL))
        else:
          height = min(height + 1, math.ceil(COLORMAX / COLORINTERVAL))
        heights[coords] = height
        color = heightToColor(height)
        drawRectFromNormCoords(coords, color)
        pygame.display.update()
