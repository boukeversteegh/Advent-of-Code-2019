from collections import defaultdict

from day09.day09 import IntCodeComputerDay9


class HullPainting:

  def foobar(self):
    # [ open("input.txt").readlines()]

    panel_colors = defaultdict(lambda: 0)

    computer = IntCodeComputerDay9()
    computer.load_from_file('day11/input.txt')

    pos = (0, 0)
    dir = 0

    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    computer.debug = False

    xrange = [None, None]
    yrange = (None, None)

    while True:

      color = panel_colors[pos]
      computer.input(color)
      computer.run_program()

      if not computer.waiting_for_input:
        break

      # read output
      new_color = computer.output.pop(0)
      panel_colors[pos] = new_color

      turn = computer.output.pop(0)
      if turn == 1:
        dir = (dir + 1) % 4
      else:
        dir = (dir - 1 + 4) % 4

      dx, dy = dirs[dir]

      pos = (pos[0] + dx, pos[1] + dy)

      x, y = pos
      #
      # if xrange[0] is None:
      #   xrange[0] = min(xrange[0], x)
      #   xrange[1] = max(xrange[1], x)
      #
      # if yrange[0] is None:
      #   yrange[0] = min(yrange[0], y)
      #   yrange[1] = max(yrange[1], y)

      # drive in direction
      print("Color=%s" % color)
      print("Turn=%s" % turn)

      if computer.waiting_for_input:
        print("Waiting for input")
      else:
        print("Done")
        break

    print(len(panel_colors.values()))

    pass


# class Example(unittest.TestCase):
#


hp = HullPainting()
hp.foobar()
