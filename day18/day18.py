import os
import sys
from collections import namedtuple
from heapq import heappush, heappop

grid = {}
player = None
keys = {}
doors = {}

with open('day18/input.txt') as fh:
  lines = [line.strip() for line in fh.readlines()]
  for y, line in enumerate(lines):
    for x, c in enumerate(line):
      grid[x, y] = c
      if c == '@':
        player = x, y
        grid[x, y] = '.'
      if c in 'abcdefghijklmnopqrstuvwxyz':
        keys[c] = x, y
      if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        doors[c] = x, y


# print(grid, player, keys, doors)

def manhattan(a, b):
  ax, ay = a
  bx, by = b
  return abs(ax - bx) + abs(ay - by)


def get_min_steps_left(position, found_keys):
  steps = 0
  x, y = position

  # estimate visiting keys
  # key_dists = sorted([(manhattan(position, kp), key, kp) for key, kp in keys.items()])
  # door_dists = sorted([(manhattan(position, dp), door, dp) for door, dp in doors.items()])
  #
  # furthest_key = key_dists[-1][0]
  # further_door_key = door_dists[-1][0]
  #
  # return max(furthest_key, further_door_key)

  next_keys = sorted(
    [(key, kp) for key, kp in keys.items() if key not in found_keys],
    key=lambda key_item: manhattan(key_item[1], position)
  )

  # next_doors = sorted(
  #   [(door, dp) for door, dp in doors.items() if door not in found_keys],
  #   key=lambda door_item: manhattan(door_item[1], position)
  # )

  if not next_keys:
    return 0

  return manhattan(position, next_keys[0][1])

  # if next_door[0] in found_keys:
  #   return manhattan(position, next_door[1])
  # else:
  #   return manhattan(position, next_key[1])

  # for key, key_pos in keys.items():
  #   if key in found_keys:
  #     continue
  #   kx, ky = key_pos
  #
  #   min_distance_to_key = abs(x - kx) + abs(y - ky)
  #   steps += min_distance_to_key

  # estimate visiting doors

  return steps


# start_min_steps_left = get_min_steps_left(player, [])
# to_visit = []
# to_visit.append((
#   0 + start_min_steps_left,
#   0,
#   start_min_steps_left,
#   player,
#   [],
#   [player],
# ))

# visited = {}  # (position, nr of keys)

max_steps = 0

minx = min(grid.keys(), key=lambda p: p[0])[0]
maxx = max(grid.keys(), key=lambda p: p[0])[0]
miny = min(grid.keys(), key=lambda p: p[1])[1]
maxy = max(grid.keys(), key=lambda p: p[1])[1]

best_nr_keys = 0

i = 0


def print_maze(x, y, path):
  global grid, minx, miny, maxx, maxy
  for _y in range(miny, maxy + 1):
    for _x in range(minx, maxx + 1):
      tile = grid[_x, _y]
      is_door = tile in doors.keys()
      if (_x, _y) == (x, y):
        o = '\033[96m%s\033[0m' % '@'
      else:

        if tile in keys.keys():
          o = '\033[91m%s\033[0m' % tile
        elif (_x, _y) in path and is_door:
          o = '\033[95m%s\033[0m' % tile
        elif is_door:
          o = '\033[93m%s\033[0m' % tile
        elif (_x, _y) in path and tile == '.':
          o = '\033[42m \033[0m'
        elif tile == '#':
          o = '\033[47m \033[0m'
        elif tile == '.':
          o = ' '
        else:
          o = tile

      print(o, end='')
    print('')


key_paths = {}
key_dependencies = {}

dirs = [
  (1, 0),
  (-1, 0),
  (0, -1),
  (0, 1),
]


def get_shortest_path(start, goal):
  paths = [[start]]

  while paths:
    path = paths.pop(0)
    position = path[-1]
    x, y = position

    if position == goal:
      return path

    for dx, dy in dirs:
      n_position = (x + dx, y + dy)
      n_path = path + [n_position]

      tile = grid[n_position]
      if tile != '#' and n_position not in path:
        paths.append(n_path)


print("Calculating path to each key")
for key, key_pos in keys.items():
  print("Calculating path for key %s" % key)
  shortest_path = get_shortest_path(player, key_pos)
  key_paths[key] = shortest_path

  key_dependencies[key] = []
  for path_pos in shortest_path:
    if path_pos in doors.values():
      # check if we didn't already find a key in the path so far
      key_dependencies[key].append(grid[path_pos].lower())

moves = []

Move = namedtuple('Move', ['priority', 'total_cost', 'cost', 'r_cost', 'target_key', 'position', 'found_keys', 'path'])

print("Getting dependencies")
for key, dependencies in key_dependencies.items():
  if not dependencies:
    moves.append(Move((1,), 0, 0, None, key, player, [], []))


def actual_key_dependencies(key, found_keys):
  return [
    key_dependency for key_dependency in key_dependencies[key]
    if key_dependency not in found_keys
  ]


solutions = []

while moves:
  print("Top 3 strategies:")
  # for s in moves[0:10]:
  #   print(" - ", s)

  strategy = heappop(moves)
  priority, total_cost, cost, remaining_cost, target_key, position, found_keys, path = strategy

  print("%s + %s: %s" % (found_keys, target_key, strategy))

  key_position = keys[target_key]
  key_path = get_shortest_path(position, key_position)
  new_cost = len(path) + len(key_path) - 1

  new_found_keys = found_keys + [target_key]

  not_found_keys = [key for key in keys.keys() if key not in new_found_keys]
  next_keys = [
    key for key in not_found_keys if not actual_key_dependencies(key, new_found_keys)
  ]

  # new_total_cost = cost +

  new_priority = (
    new_cost / len(new_found_keys),  # - len(new_found_keys),
  )

  new_path = path + key_path[1:]
  for next_key in next_keys:
    # next_key_cost = get_shortest_path(keys[next_key])
    heappush(moves, Move(
      new_priority,
      total_cost,
      new_cost,
      0,  # remaining cost
      next_key,
      key_position,
      new_found_keys,
      new_path
    ))

  os.system('clear')

  # print_maze(position[0], position[1], new_path)
  if not not_found_keys:
    print("Done! Total cost: %s" % (new_cost))

    solutions.append((new_cost, new_found_keys))
    # break

    print("Continue searching for more?")
    breakpoint()

solutions = sorted(solutions)

sys.exit()


def search_next_key():
  debug_mode = 'a'
  while len(to_visit):
    further = False
    more_steps = False
    more_keys = False

    min_total_steps, steps, min_steps_left, (x, y), found_keys, path = heappop(to_visit)

    visited_key = ((x, y), tuple(sorted(found_keys)))
    if visited_key not in visited or visited[visited_key] < steps:
      visited[visited_key] = steps

    if steps > max_steps:
      max_steps = steps
      more_steps = True

    if (len(found_keys) > best_nr_keys):
      more_keys = True
      best_nr_keys = len(found_keys)

    # if (not found_keys and more_steps) or more_keys:
    if more_keys:
      further = True

    # find other locations

    # check target is goal
    reached_goal = len(found_keys) == len(keys)

    # Check locations to visit
    near_open_door = False
    if not reached_goal:
      for (dx, dy) in dirs:
        nx, ny = x + dx, y + dy
        tile = grid[nx, ny]
        is_empty = tile == '.'
        is_key = tile in keys.keys()
        is_door = tile in doors.keys()
        is_open_door = is_door and tile.lower() in found_keys
        if is_open_door:
          near_open_door = True
        can_visit = is_empty or is_key or is_open_door

        if can_visit:
          found_key = [tile] if is_key else []
          n_found_keys = list(set(found_keys + found_key))

          dir_min_steps_left = get_min_steps_left((nx, ny), n_found_keys)

          n_steps = (steps + 1)
          n_visited_key = (nx, ny), tuple(sorted(n_found_keys))
          if n_visited_key not in visited or n_steps < visited[n_visited_key]:
            heappush(to_visit, (
              n_steps + dir_min_steps_left,
              n_steps,
              dir_min_steps_left,
              (nx, ny),
              n_found_keys,
              path + [(x, y)]
            ))

    breaking = False
    if debug_mode == 'a':
      breaking = True
    if debug_mode == 'k':
      breaking = more_keys
    if debug_mode == 's':
      breaking = more_steps
    if debug_mode == 'd':
      breaking = near_open_door
    if debug_mode == 'g':
      breaking = reached_goal
    if debug_mode == 'e':
      breaking = False

    if breaking:
      os.system('clear')
      print_maze(x, y, path)

      print('Evaluated #%s:' % (i + 1,))
      # print(' - [%s,%s] %s / %s %s' % (steps + min_steps_left, steps, min_steps_left, (x, y), found_keys, '%s positions left' % len(to_visit))
      print('   [%s,%s] %s / %s %s' % (x, y, steps, min_total_steps, found_keys))
      print('')

      new_debug_mode = None
      while new_debug_mode == None:
        new_debug_mode = input(
          'Debug? [a=always wait, k=next key, s=more steps, d=near open door, g=goal, e=end]: ').strip()
        if new_debug_mode == 'p':
          print("Future options:")
          for _v in range(0, min(4, len(to_visit) - 1) + 1):
            v_min_total_steps, v_steps, v_min_steps_left, (v_x, v_y), v_found_keys, _ = to_visit[_v]
            print(' - [%s,%s] %s / %s %s' % (v_x, v_y, v_steps, v_min_total_steps, v_found_keys))
          new_debug_mode = None
        elif len(new_debug_mode) > 0:
          debug_mode = new_debug_mode
      print('')
    i += 1

    if reached_goal:
      print("Reached goal in %s steps" % steps)
      break

for x in range(0, 10):
  pass
