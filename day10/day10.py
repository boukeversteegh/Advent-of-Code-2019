import collections
import math

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

    print(groups)

    print((cx, cy))
    # for y, row in enumerate(rows):
    #   for (x, pos) in enumerate(row):
    #     if (x, y) in asteroids:
    #
    #       a_groups = [key for key, group in groups.items() if (x, y) in group]
    #       if a_groups != []:
    #         print(chr(65 + list(groups.keys()).index(a_groups[0])), end='')
    #       else:
    #         print('#', end='')
    #     else:
    #       print('.', end='')
    #   print('')
    # print('-----')

    print('Group/asteroid count: %s' % len(groups))
    candidate_group_counts.append([(cx, cy), len(groups)])

  print(candidate_group_counts)

  print(max(candidate_group_counts, key=lambda entry: entry[1]))

  # 264 BAD
  # 265 BAD
  # 272 BAD #5
  # 274 BAD <--- Right answer probably lol
  # 289 BAD
  # 290 BAD
