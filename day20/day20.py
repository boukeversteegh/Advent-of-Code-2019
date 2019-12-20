import os
from time import sleep

walkable_tiles = set()

portals = {}
portal_positions = {}

input_file = 'day20/input.txt'
portal_letters = {}

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
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


def print_maze(x, y, path):
  for _y, row in enumerate(grid):
    for _x, tile in enumerate(row.rstrip('\n')):
      if (_x, _y) == (x, y):
        o = '\033[96m%s\033[0m' % '@'
      else:
        if (_x, _y) in path:
          o = '\033[42m \033[0m'
        elif tile == '#':
          o = '\033[47m \033[0m'
        elif tile == '.':
          o = '.'
        else:
          o = tile

      print(o, end='')
    print('')

with open(input_file) as fh:
  grid = [line for line in fh.readlines()]

  for y, row in enumerate(grid):
    for x, tile in enumerate(row):
      if tile == '.':
        walkable_tiles.add((x, y))

        for dx, dy in dirs:
          px, py = x + dx, y + dy
          px2, py2 = x + dx * 2, y + dy * 2
          p = (px, py)

          print(p)

          if px2 in range(0, len(row)) and py2 in range(0, len(grid)) and grid[py][px] in letters:
            if dx < 0 or dy < 0:
              name = grid[py2][px2] + grid[py][px]
            else:
              name = grid[py][px] + grid[py2][px2]

            if name == 'AA':
              start = x, y
            if name == 'ZZ':
              end = x, y

            if name in portal_positions:
              other_portal_entrance, other_portal_tile = portal_positions[name]
              portals[p] = other_portal_tile
              portals[other_portal_entrance] = (x, y)
            else:
              portal_positions[name] = (p, (x, y))

print(portal_positions, portals)


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

def part2():
  check_tiles = [
    [start + (0,)]
  ]
  i = 0
  while check_tiles:
    path = check_tiles.pop(0)
    x, y, z = path[-1]

    if i % 1000 == 0:
      os.system('clear')
      print('#%s' % i)
      #   print_maze(x, y, [(x, y) for x, y, z in path])
      print("Level: %s" % z)
    #   print(path)
    # sleep(0.1)

    for dx, dy in dirs:
      nx, ny = x + dx, y + dy
      n = (nx, ny)

      is_portal_start = (nx, ny) in portals
      is_outer_portal = is_portal_start and \
                        (nx == 2 or nx > len(grid[2]) - 2 or
                         ny == 2 or ny > len(grid[2]) - 2)

      is_inner_portal = is_portal_start and not is_outer_portal

      at_top = z == 0

      if is_outer_portal and at_top:
        continue

      if is_portal_start:
        tx, ty = portals[nx, ny]

        if is_outer_portal and not at_top:
          tz = z - 1
        if is_inner_portal:
          tz = z + 1

        if (tx, ty, tz) not in path:
          check_tiles.append(path + [(tx, ty, tz)])

      else:
        if (nx, ny) in walkable_tiles and (nx, ny, z) not in path:
          check_tiles.append(path + [(nx, ny, z)])

    if end == (x, y) and z == 0:
      print_maze(x, y, [(x, y) for x, y, z in path])
      print("Reached ZZ")
      print(path)
      print("Path length, excluding start: ", len(path) - 1)

      break

    i += 1


part2()
