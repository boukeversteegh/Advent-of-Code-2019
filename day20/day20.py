import os
import string
import sys
from collections import deque
from time import sleep

walkable_tiles = set()

portals = {}
portal_positions = {}

input_file = 'day20/input.txt'
portal_letters = {}

letters = string.ascii_letters
horizontal_wall_size = None
wall_width = None

dirs = [
  (1, 0),
  (-1, 0),
  (0, -1),
  (0, 1),
]

start = None
end = None

outer_portals = set()
inner_portals = set()

with open(input_file) as fh:
  grid = [line for line in fh.readlines()]
  h = len([_ for _ in grid if len(_.strip()) > 0])
  w = max([len(l.strip()) for l in grid])

  for y, row in enumerate(grid):
    for x, tile in enumerate(row):
      if tile == '.':
        walkable_tiles.add((x, y))

        for dx, dy in dirs:
          px, py = x + dx, y + dy
          px2, py2 = x + dx * 2, y + dy * 2
          p = (px, py)
          p2 = px2, py2

          print(p)

          if px2 in range(0, w) and py2 in range(0, h) and grid[py][px] in letters:
            if dx < 0 or dy < 0:
              name = grid[py2][px2] + grid[py][px]
            else:
              name = grid[py][px] + grid[py2][px2]

            if name == 'AA':
              start = x, y
            if name == 'ZZ':
              end = x, y

            if min(w - px, px, h - py, py) in [1, 2]:
              outer_portals.add(p)
              outer_portals.add(p2)
            else:
              inner_portals.add(p)
              inner_portals.add(p2)

            if name in portal_positions:
              other_portal_entrance, other_portal_tile = portal_positions[name]
              portals[p] = other_portal_tile
              portals[other_portal_entrance] = (x, y)
            else:
              portal_positions[name] = (p, (x, y))

print(portal_positions, portals)


def print_maze(x, y, z, path):
  path2d_current_level = set([(_x, _y) for _x, _y, _z in path if _z == z])
  path2d_other_level = set([(_x, _y) for _x, _y, _z in path if _z != z])
  for _y, row in enumerate(grid):
    for _x, tile in enumerate(row.rstrip('\n')):
      if (_x, _y) == (x, y):
        o = '\033[96m%s\033[0m' % '@'
      else:
        if (_x, _y) in path2d_current_level:
          o = '\033[102m \033[0m'
        elif (_x, _y) in path2d_other_level:
          o = '\033[42m \033[0m'
        elif tile == '#':
          o = '\033[47m \033[0m'
        elif tile == '.':
          o = '.'
        elif (_x, _y) in outer_portals:
          o = '\033[95m%s\033[0m' % tile
        elif (_x, _y) in inner_portals:
          o = '\033[91m%s\033[0m' % tile
        else:
          o = tile
      sys.stdout.buffer.write(str.encode(o))
    sys.stdout.buffer.write(b'\n')
  sys.stdout.buffer.flush()


def part1():
  check_tiles = [
    [start]
  ]
  i = 0
  while check_tiles:
    path = check_tiles.pop(0)
    x, y = path[-1]

    if i % 1000 == 0:
      os.system('clear')
      print_maze(x, y, path)
      sleep(0.1)
      # print(path)

    for dx, dy in dirs:
      nx, ny = x + dx, y + dy

      is_portal_start = (nx, ny) in portals

      if (nx, ny) not in path and not (is_portal_start and portals[nx, ny] in path):
        if (nx, ny) in walkable_tiles:
          check_tiles.append(path + [(nx, ny)])
        if is_portal_start:
          check_tiles.append(path + [portals[nx, ny]])

    if end == (x, y):
      print("Reached ZZ")
      print(path)
      print("Path length, excluding start: ", len(path) - 1)
      break

    i += 1


# part 1
# 637 too high
# 636 too high

if start == None:
  raise Exception("No start found")

if end == None:
  raise Exception("No end found")


def part2():
  check_tiles = deque([
    [start + (0,)]
  ])
  checked_tiles = {}
  i = 0
  while check_tiles:
    path = check_tiles.popleft()
    x, y, z = path[-1]

    if i % 100000 == 0:
      os.system('clear')
      print('#%s/%s' % (i, len(check_tiles)))
      print("Level: %s" % z)
      print_maze(x, y, z, checked_tiles.keys())

    for dx, dy in dirs:
      nx, ny = x + dx, y + dy
      nz = z

      is_portal_start = (nx, ny) in portals
      is_outer_portal = is_portal_start and (nx, ny) in outer_portals
      is_inner_portal = is_portal_start and (nx, ny) in inner_portals

      at_top = z == 0

      if is_outer_portal and at_top:
        continue

      if is_portal_start:
        nx, ny = portals[nx, ny]

        if is_outer_portal and not at_top:
          nz = z - 1
        if is_inner_portal:
          nz = z + 1

      if (nx, ny) in walkable_tiles and (nx, ny, nz) not in checked_tiles:
        # Essential! Keep as 'checked' as soon as possible!
        checked_tiles[(nx, ny, nz)] = len(path) + 1

        check_tiles.append(path + [(nx, ny, nz)])

    if end == (x, y) and z == 0:
      print_maze(x, y, z, path)
      print("Reached ZZ")
      print(path)
      print("Path length, excluding start: ", len(path) - 1)

      break

    if i % 1000 == 0:
      print('#%s/%s\r' % (i, len(check_tiles)), end='')
    i += 1


part2()
