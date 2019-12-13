from collections import defaultdict

from day09.day09 import IntCodeComputerDay9

EMPTY = 0
WALL = 1
BLOCK = 2
HORIZONTAL = 3
BALL = 4

NEUTRAL = 0
LEFT = -1
RIGHT = 1


class ArcadeCabinet:

  def part1(self):
    score = 0
    screen = defaultdict(lambda: EMPTY)

    computer = IntCodeComputerDay9()
    computer.load_from_file('day13/input.txt')

    computer.debug = False

    computer.positions[0] = 2
    computer.run_program()

    while computer.output != []:
      x = computer.output.pop(0)
      y = computer.output.pop(0)
      t = computer.output.pop(0)

      if y == -1 and x == 0:
        score = t
      else:
        screen[(x, y)] = t

    print(len([t for t in screen.values() if t == BLOCK]))


machine = ArcadeCabinet()
machine.part1()
