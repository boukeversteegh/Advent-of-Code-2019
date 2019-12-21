from day09.day09 import IntCodeComputerDay9


class SpringDroid:
  def __init__(self):
    self.computer = IntCodeComputerDay9()
    self.computer.debug = False
    self.computer.load_from_file('day21/input.txt')
    self.program = None

  def load_program(self, program):
    self.program = program.lstrip("\n")

  def start(self):
    for c in self.program:
      self.computer.input(ord(c))

    self.computer.run_program()

    print(self.program)

    for c in self.computer.output:
      if c <= 127:
        print(chr(c), end='')
      else:
        print("Steps", c)


droid = SpringDroid()
droid.load_program("""
NOT C J
AND D J
NOT A T
OR T J
WALK
""")
droid.start()
