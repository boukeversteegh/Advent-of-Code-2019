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

# TILE_SIZE = 8
# display = pygame.display.set_mode((42 * TILE_SIZE, 22 * TILE_SIZE), 0, 32)

TILES = [
  ' ',
  '#',
  'X',
  '-',
  'O',
]


class ArcadeCabinet:
  def __init__(self):
    self.screen = defaultdict(lambda: EMPTY)
    self.score = 0
    self.size = 43, 23

    self.ball = (None, None)
    self.ball_dir = (1, 0)
    self.player = (None, None)
    self.i = 0

  def draw(self, draw=True):
    if draw:
      print('Score: %s' % self.score)
    w, h = self.size
    self.blocks = 0
    self.i += 1
    for y in range(0, h):
      if draw:
        print(str(y).rjust(4, ' ') + ' ', end='')
      for x in range(0, w):
        tile_id = self.screen[x, y]
        tile_image = TILES[tile_id]
        if tile_id == BALL:
          if self.ball[0] is not None:
            self.ball_dir = (x - self.ball[0], y - self.ball[1])
          self.ball = (x, y)

        if tile_id == HORIZONTAL:
          self.player = (x, y)
        if tile_id == BLOCK:
          self.blocks += 1
        if draw:
          print(tile_image, end='')
      if draw:
        print('')
    if self.i % 100 == 0:
      print("Blocks left: %s" % self.blocks)

  def part1(self):

    computer = IntCodeComputerDay9()
    computer.load_from_file('day13/input.txt')

    computer.debug = False

    computer.positions[0] = 2

    while True:
      computer.run_program()

      while computer.output:
        x = computer.output.pop(0)
        y = computer.output.pop(0)
        t = computer.output.pop(0)

        if x == -1 and y == 0:
          self.score = t
        else:
          self.screen[(x, y)] = t

      self.draw(draw=False)

      if computer.waiting_for_input:
        # AI
        ball_x = self.ball[0]
        px = self.player[0]

        dy = self.player[1] - self.ball[1]

        if self.ball_dir[1] < 0:
          dy *= 2

        dx = px - ball_x

        ball_tx = ball_x + self.ball_dir[0] * dy

        # print({"px": px, "ball_x": ball_x, "ball_tx": ball_tx})
        if px < ball_tx - 1:
          # left of ball target
          # print("Right")
          computer.input(1)
        elif px > ball_tx + 1:
          # print("Left")
          computer.input(-1)
        else:
          # print("HOLD")
          computer.input(0)
        # sleep(0.3)
        continue

      else:
        break

    print(len([t for t in self.screen.values() if t == BLOCK]))
    print(max(self.screen.keys()))
    self.draw(draw=True)
    print(self.score)


machine = ArcadeCabinet()
machine.part1()
