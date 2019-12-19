import collections
import os

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


start_min_steps_left = get_min_steps_left(player, [])
to_visit = collections.deque()
to_visit.append((
  0 + start_min_steps_left,
  0,
  start_min_steps_left,
  player,
  [],
  [player],
))

visited = {}  # (position, nr of keys)

max_steps = 0

minx = min(grid.keys(), key=lambda p: p[0])[0]
maxx = max(grid.keys(), key=lambda p: p[0])[0]
miny = min(grid.keys(), key=lambda p: p[1])[1]
maxy = max(grid.keys(), key=lambda p: p[1])[1]

best_nr_keys = 0

i = 0

break_condition = 'a'
while len(to_visit):
  further = False
  more_steps = False
  more_keys = False

  # for _v in range(0, min(10, len(to_visit) - 1)):
  #   print(' -', to_visit[_v])

  min_total_steps, steps, min_steps_left, (x, y), found_keys, path = to_visit.popleft()

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
  dirs = [
    (1, 0),
    (-1, 0),
    (0, -1),
    (0, 1),
  ]

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
          to_visit.append((
            n_steps + dir_min_steps_left,
            n_steps,
            dir_min_steps_left,
            (nx, ny),
            n_found_keys,
            path + [(x, y)]
          ))

  breaking = False
  if break_condition == 'a':
    breaking = True
  if break_condition == 'k':
    breaking = more_keys
  if break_condition == 's':
    breaking = more_steps
  if break_condition == 'd':
    breaking = near_open_door
  if break_condition == 'g':
    breaking = reached_goal
  if break_condition == 'e':
    breaking = False

  if breaking:
    os.system('clear')
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

    print('')
    print(steps + min_steps_left, steps, min_steps_left, (x, y), found_keys, '%s positions left' % len(to_visit))
    print('')
    new_break_condition = input(
      'Wait when? [a=always wait, k=next key, s=more steps, d=near open door, g=goal, e=end]: ').strip()
    if len(new_break_condition) > 0:
      break_condition = new_break_condition
    print('')
  i += 1

  if reached_goal:
    print("Reached goal in %s steps" % steps)
    break
# for y, x in sorted([(y, x) for x, y in grid.keys()]):
#   print(grid[x, y])

for x in range(0, 10):
  pass
