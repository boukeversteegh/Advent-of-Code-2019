from day09.day09 import IntCodeComputerDay9

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

WALL = 0
EMPTY = 1
GOAL = 2
UNEXPLORED = 3

computer = IntCodeComputerDay9()
computer.debug = False
computer.load_from_file('day15/input.txt')

directions = {
  NORTH: (0, -1),
  SOUTH: (0, 1),
  WEST: (-1, 0),
  EAST: (1, 0),
}

direction_order = [NORTH, EAST, SOUTH, WEST]  # reversing directions

visited = {
  (0, 0): (EMPTY, None)
}

to_visit = [
  # Direction from starting point, target destination
  (NORTH, directions[NORTH], (0, 0)),
  (SOUTH, directions[SOUTH], (0, 0)),
  (WEST, directions[WEST], (0, 0)),
  (EAST, directions[EAST], (0, 0)),
]

# grid = defaultdict(lambda: defaultdict(lambda: UNEXPLORED))

while True:
  # print(to_visit)
  # os.system('clear')
  # print(chr(27) + "[;H")
  (direction, target_position, previous_position) = to_visit.pop(0)
  print("Going %s, visiting %s" % (' NSWE'[direction], target_position))
  computer.input(direction)

  computer.run_program()
  status = computer.output.pop(0)

  visited[target_position] = (status, direction)

  print("Found: [%s]" % ('#.* '[status]))

  # backtrack
  if status != WALL:
    x, y = target_position
    opposite_direction = direction_order[((direction_order.index(direction) + 2) % 4)]
    print("    Backtracking %s" % 'xNSWE'[opposite_direction])
    computer.input(opposite_direction)
    computer.run_program()

    for direction, (dx, dy) in directions.items():
      to_visit_position = (target_position[0] + dx, target_position[1] + dy)
      if to_visit_position not in visited.keys():
        to_visit.append((direction, to_visit_position, target_position))
        print("Appending %s to list" % (to_visit_position,))
  else:
    x, y = previous_position

  if status == GOAL:
    break

  ypositions = [y for x, y in visited.keys()]
  xpositions = [x for x, y in visited.keys()]

  miny = min(ypositions)
  maxy = max(ypositions)
  minx = min(xpositions)
  maxx = max(xpositions)

  to_visit_positions = [pos for _, pos, _ in to_visit]

  for _y in range(miny - 1, maxy + 2):
    for _x in range(minx - 1, maxx + 2):
      pos = _x, _y
      if pos in visited:
        s = visited[(_x, _y)][0]
      else:
        s = UNEXPLORED
      if x == _x and y == _y:
        print('@', end='')
      else:
        if (_x, _y) in to_visit_positions:
          print('?', end='')
        else:
          print('#.* '[s], end='')
    print('')

  continue
