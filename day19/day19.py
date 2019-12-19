from day07.day07 import AmpRunner
from day09.day09 import IntCodeComputerDay9

computer = IntCodeComputerDay9()

program = AmpRunner.load_program_from_file('day19/input.txt')
computer.debug = False

yes = 0
inputs = []
# for y in range(0, 50):
#   for x in range(0, 50):
#     computer.run_program(program=program, inputs=[x, y])
#     in_beam = computer.output[0]
#     if in_beam == 1:
#       yes += 1
#     print("#" if in_beam else '.', end='')
#   print()
# breakpoint()

print(yes)

# ship size 2
# 0 0 (0, 0) (1, 0)
# 0 0

ship_size = 100


# ship_size = 2

def in_ship(ship_x, ship_y, x, y):
  return x in range(ship_x, ship_x + (ship_size)) and y in range(ship_y, ship_y + (ship_size))


def in_beam(pos):
  x, y = pos
  computer.run_program(program=program, inputs=[x, y])
  return computer.output[0] == 1


margin = 2


def print_ship(x, y):
  for _y in range(y - margin, y + ship_size + margin):
    for _x in range(x - margin, x + ship_size + margin):
      if in_ship(x, y, _x, _y):
        print('+', end='')
      else:
        print('#' if in_beam((_x, _y)) else '.', end='')
    print()


x, y = 0, 0
x, y = 33, 49
# x, y = 1147, 1642

fully_in_beam = False
while True:
  tl = x, y
  bl = x, y + (ship_size - 1)
  br = x + (ship_size - 1), y + (ship_size - 1)
  tr = x + (ship_size - 1), y

  if not fully_in_beam and not in_beam(bl):
    print("%s, %s bottom left is not in beam. going right" % (x, y))
    # print_ship(x, y)
    x += 1
  elif not fully_in_beam and not in_beam(tr):
    print("%s, %s top right not in beam. going down" % (x, y))
    # print_ship(x, y)
    y += 1
  else:
    fully_in_beam = True
    tr_outside = tr[0], tr[1] - 1
    bl_outside = bl[0] - 1, bl[1]

    tr_up_left = tr[0] - 1, tr[1] - 1
    bl_up_left = bl[0] - 1, bl[1] - 1

    tr_up2_left = tr[0] - 1, tr[1] - 2
    bl_up2_left = bl[0] - 1, bl[1] - 2

    if in_beam(tr_outside):
      print("[%s, %s] In beam now. But we need to go up a bit" % (x, y))
      # print_ship(x, y)
      y -= 1
      continue

    if in_beam(bl_outside):
      x -= 1
      print("[%s, %s] In beam now. But we need to go left a bit" % (x, y))
      # print_ship(x, y)
      continue

    if in_beam(tr_up_left) and in_beam(bl_up_left):
      x -= 1
      y -= 1
      print("[%s, %s] In beam now. Let's jump up and left by 1" % (x, y))
      continue

    if in_beam(tr_up2_left) and in_beam(bl_up2_left):
      x -= 1
      y -= 2
      print("[%s, %s] In beam now. Let's jump up 2 and left by 1" % (x, y))
      continue

    break

print(x, y)

# 1147 1642
# 1143 1636
# 1137 1628
# 1135 1625
print_ship(x, y)

# 11471642 #incorrect
