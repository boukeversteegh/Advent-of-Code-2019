# 1621

# direct: 1620
# indirect: 1620+1619+1618

# 1313010
# 1314630
from collections import defaultdict

lines = open("input.txt").readlines()

parents = {}

orbits = defaultdict(lambda: [])
paths = {}
for line in lines:
  parent, child = line.strip().split(')')
  orbits[parent].append(child)


def load_paths(node, path):
  paths[node] = path
  children = orbits[node]
  for child in children:
    load_paths(child, path + [node])
    # paths[child] = path + [node]


load_paths('COM', [])

print(sum([len(path) for path in paths.values()]))

# COM

# 1621 BAD
