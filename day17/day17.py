from day09.day09 import IntCodeComputerDay9

computer = IntCodeComputerDay9()

computer.load_from_file('day17/input.txt')

computer.debug = False
computer.run_program()

chars = computer.output

y = 0
x = 0
scaffolds = set()
for c in chars:
  if chr(c) == "\n":
    y += 1
    x = 0
    continue

  if chr(c) == '#':
    scaffolds.add((x, y))

  x += 1

s_alignment_params = 0

minx = min(scaffolds, key=lambda p: p[0])[0]
miny = min(scaffolds, key=lambda p: p[1])[1]

for x, y in scaffolds:
  neighbors = [
    (1, 0),
    (-1, 0),
    (0, -1),
    (0, 1),
  ]

  intersection = True
  for dx, dy in neighbors:
    nx, ny = x + dx, y + dy
    if not (nx, ny) in scaffolds:
      intersection = False
      break

  if intersection:
    rx = x - minx
    ry = y - miny
    s_alignment_params += rx * ry

print(scaffolds)
print(s_alignment_params)
