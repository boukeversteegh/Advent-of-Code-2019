from day09.day09 import IntCodeComputerDay9

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

WALL = 0
EMPTY = 1
GOAL = 2
UNEXPLORED = 3

robot = IntCodeComputerDay9()
robot.debug = False
robot.load_from_file('day15/input.txt')

directions = {
  NORTH: (0, -1),
  SOUTH: (0, 1),
  WEST: (-1, 0),
  EAST: (1, 0),
}

direction_order = [NORTH, EAST, SOUTH, WEST]  # reversing directions

visited = {
  (0, 0): (EMPTY, None, 0)
}

to_visit = [
  # Direction from starting point, target destination
  (NORTH, directions[NORTH], (0, 0)),
  (SOUTH, directions[SOUTH], (0, 0)),
  (WEST, directions[WEST], (0, 0)),
  (EAST, directions[EAST], (0, 0)),
]

robot_states = {(0, 0): robot.get_state()}

# robot.debug = True
while True:
  # print(to_visit)
  # os.system('clear')
  # print(chr(27) + "[;H")
  (direction, target_position, base_position) = to_visit.pop(0)
  print('-------------------------------')
  print("[%s -> %s (%s)]" % (base_position, target_position, ' NSWE'[direction]))

  robot_state = robot_states[base_position]

  # for old_state, current_state in zip(robot_state.inputs, robot.inputs):
  #   if old_state

  state_different = False

  robot.load_state(robot_state)
  if robot.inputs:
    raise ValueError("Already got input %s" % robot.inputs)

  if robot.output:
    raise ValueError("Already got output %s" % robot.output)

  if target_position in visited:
    raise ValueError("Already visited %s" % target_position)

  robot.input(direction)
  robot.run_program()

  for a, b in zip(robot_state.positions, robot.positions):
    if a != b:
      state_different = True
  print("Ran robot. State different: %s" % state_different)

  status = robot.output.pop(0)

  print("Found: [%s]" % ('#.* '[status]))

  _, _, previous_steps = visited[base_position]
  steps = previous_steps + 1
  visited[target_position] = (status, direction, steps)

  # backtrack
  if status != WALL:
    x, y = target_position
    robot_states[target_position] = robot.get_state()

    to_visit_positions = [pos for _, pos, _ in to_visit]
    for direction, (dx, dy) in directions.items():
      to_visit_position = (x + dx, y + dy)
      if to_visit_position not in visited.keys() and to_visit_position not in to_visit_positions:
        to_visit.append((direction, to_visit_position, target_position))
        print("Appending %s to list" % (to_visit_position,))
  else:
    x, y = base_position

  if status == GOAL:
    print((steps, (x, y)))
    break

  ypositions = [y for x, y in visited.keys()]
  xpositions = [x for x, y in visited.keys()]

  miny = min(ypositions)
  maxy = max(ypositions)
  minx = min(xpositions)
  maxx = max(xpositions)

  to_visit_positions = [pos for _, pos, _ in to_visit]

  # for _y in range(miny - 1, maxy + 2):
  #   print(str(_y).rjust(3, ' ') + ' ', end='')
  #   for _x in range(minx - 1, maxx + 2):
  #     pos = _x, _y
  #     if pos in visited:
  #       s = visited[(_x, _y)][0]
  #     else:
  #       s = UNEXPLORED
  #     if x == _x and y == _y:
  #       print('@', end='')
  #     else:
  #       if (_x, _y) in to_visit_positions:
  #         print('?', end='')
  #       else:
  #         print('#.* '[s], end='')
  #   print('')

  continue
