from day09.day09 import IntCodeComputerDay9


class SpringDroid:
  def __init__(self):
    self.computer = IntCodeComputerDay9()
    self.computer.debug = False
    self.computer.load_from_file('day21/input.txt')
    self.program = None

  def load_program(self, program):
    self.program = [line for line in program.lstrip("\n").split('\n') if not line.startswith('#') and line != '']

  def start(self):
    print(self.program)
    print(len(self.program), 'lines')
    for line in self.program:
      for c in line:
        self.computer.input(ord(c))
      self.computer.input(10)

    self.computer.run_program()

    line = ''
    x = None
    for c in self.computer.output:
      if c <= 127:
        line += chr(c)
      else:
        print("Steps", c)
        break

      if chr(c) == '@':
        x = len(line)

      if c == 10:
        print(line, end='')
        if '#' in line:
          print(' ' * x + 'ABCDEFGHI')
        line = ''


droid = SpringDroid()
# droid.load_program("""
# NOT C J
# AND D J
# NOT A T
# OR T J
# WALK
# """)
droid.load_program("""
OR D J

# reset T
NOT A T
AND A T

OR B T
OR E T
NOT T T
OR T J


# Cancel if we would need to do a double jump
# ##.#.#..
# ABCDEFGH
#
# NOT C
# NOT E
# NOT H

# reset T
NOT A T
AND A T


#
# ....@............
# #####.##.###.####
#      ABCDEFGH


RUN
""")
# @
# #??.#.??#?????
#  ABCDEFGH
#
# ##.#.#..
# ABCDEFGH
# @
# ###.#
#  ABCD

# 1...2............
# #####.##.##
#  ABCDEFGH

droid.load_program("""
OR D J

NOT A T
AND A T

# four walls then dont jump?

OR A T
AND B T
AND C T
AND D T
NOT T T
AND T J

# .................
# .................
# ..@..............
# #####.#.#...#.###
#    ABCDEFGHI
# 
# E and H are holes then dont jump

NOT A T
AND A T
OR E T
OR H T

AND T J

RUN
""")
droid.start()
