import collections
import math


def print_map(asteroids, groups):
  for y, row in enumerate(rows):
    for (x, pos) in enumerate(row):
      if (x, y) in asteroids:

        a_groups = [key for key, group in groups.items() if (x, y) in group]
        if a_groups != []:
          print(chr(65 + list(groups.keys()).index(a_groups[0])), end='')
        else:
          print('#', end='')
      else:
        print('.', end='')
    print('')
  print('-----')

with open('day10/input.txt') as fh:
  rows = [line.strip() for line in fh.readlines()]
  w = len(rows[0])
  h = len(rows)

  print("Size : %s * %s" % (w, h))

  asteroids = []

  for y, row in enumerate(rows):
    for (x, y) in [(x, y) for (x, pos) in enumerate(row) if pos != '.']:
      asteroids.append((x, y))

  candidate_group_counts = []
  candidate_groups = {}
  for cx, cy in asteroids:
    _ = 1
    groups = collections.defaultdict(lambda: [])

    for other in asteroids:
      if other == (cx, cy):
        continue

      ox, oy = other

      dx, dy = ox - cx, oy - cy

      if dx == 0 and dy != 0:
        # vertical     |
        # vertical     |
        # vertical     |
        group = (cx, -1 if dy < 0 else 1)
        groups[group].append((ox, oy))

      if dy == 0 and dx != 0:
        # horizontal ------
        group = (-1 if dx < 0 else 1, cy)
        groups[group].append((ox, oy))

      if dx != 0 and dy != 0:
        _gcd = math.gcd(dx, dy)
        vector = dx / _gcd, dy / _gcd
        group = vector

        groups[group].append((ox, oy))

    print((cx, cy))

    # print_map(asteroids, groups)

    candidate_group_counts.append([(cx, cy), len(groups)])
    candidate_groups[(cx, cy)] = groups

  # print(candidate_group_counts)

  # part 1

  # 264 BAD
  # 265 BAD
  # 272 BAD #5
  # 274 BAD <--- Right answer probably lol
  # 289 BAD
  # 290 BAD

  # Part 2
  (x, y), count = max(candidate_group_counts, key=lambda entry: entry[1])
  print((x, y), count)

  groups = candidate_groups[x, y]


  def dist(a, b):
    ax, ay = a
    bx, by = b
    return math.sqrt(pow(ax - bx, 2) + pow(ay - by, 2))


  def angle(a, b):
    ax, ay = a
    bx, by = b
    dx = ax - bx
    dy = ay - by
    return (math.degrees(math.atan2(dy, dx)) - 90 + 360) % 360


  groups = [sorted(group, key=lambda group: dist(group, (x, y))) for group in groups.values()]

  groups = sorted(groups, key=lambda group: angle((x, y), group[0]))


  def part2(groups):
    count = 0
    while True:
      print_map(asteroids, {index: group for index, group in enumerate(groups)})
      groups = [group for group in groups if len(group) > 0]
      if (len(groups) == 0):
        break

      print("Iterating over %s non-empty groups" % (len(groups)))

      for group in groups:
        if group == []:
          continue

        print(group)
        nearest = group.pop(0)
        print("popped %s" % (nearest,))
        print_map(asteroids, {index: group for index, group in enumerate(groups)})

        count += 1
        # print(count, nearest)

        if count == 200:
          print("DONE", nearest)
          return


  part2(groups)

  # (3, 5) -> 305 Correct
