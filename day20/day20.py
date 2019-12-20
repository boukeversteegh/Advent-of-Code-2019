empty = set()

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

with open(input_file) as fh:
  grid = [line for line in fh.readlines()][:-1]

  for y, row in enumerate(grid):
    for x, tile in enumerate(row):
      if tile == '.':
        empty.add((x, y))

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

            if name in portal_positions:
              other_portal = portal_positions[name]
              portals[p] = other_portal
              portals[other_portal] = p
            else:
              portal_positions[name] = px, py

print(portal_positions, portals)
