import collections

raw = open('input.txt').readlines()

# raw = ['R8,U5,L5,D3', 'U7,R6,D4,L4']
# raw = ['R75,D30,R83,U83,L12,D49,R71,U7,L72',
#        'U62,R66,U55,R34,D71,R55,D58,R83']

lines = [line.strip() for line in raw]

grid = collections.defaultdict(lambda: collections.defaultdict(lambda: {}))

# (lbound, rbound, ubound, bbound) = (0,0,0,0)

for line_index, line in enumerate(lines):
  sections = line.split(',')

  x, y = (0, 0)
  for section in sections:
    # print(section)
    section_direction = section[0]
    section_dist = int(section[1:])

    section_dx = 0
    section_dy = 0

    if section_direction == 'U':
      section_dy -= 1
    if section_direction == 'D':
      section_dy += 1
    if section_direction == 'L':
      section_dx -= 1
    if section_direction == 'R':
      section_dx += 1

    section_tx, section_ty = (x + section_dx, y + section_dy)

    for i in range(0, section_dist):
      x += section_dx
      y += section_dy
      # print("Step %s: %s,%s" % (i, x, y))

      grid[y][x][line_index] = True

min_x = 0
min_y = 0
min_distance = None
# nearest_intersection = None


for y, row in grid.items():
  for x, lines in row.items():
    if len(lines.items()) > 1:
      distance = abs(x) + abs(y)
      if min_distance is None or (distance < min_distance):
        print("Intersection at %s" % (((x, y), distance),))
        min_x = x
        min_y = y
        min_distance = distance

print(((min_x, min_y), min_distance))

# class Intersector:
#
#   def load(self, wires):
#


# 2923 WRONG
# 399  RIGHT
