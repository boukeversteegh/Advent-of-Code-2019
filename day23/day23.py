import sys

from day09.day09 import IntCodeComputerDay9


class NIC:
  def __init__(self, address, program):
    self.address = address

    computer = IntCodeComputerDay9(self.address)
    computer.load(program)
    computer.debug = False

    def default_input():
      while True:
        yield -1
        # sleep(0.1)

    # computer.input_generator = default_input()

    self.computer = computer
    self.input_buffer = []
    self.output_buffer = []
    self.nics = []

  def output_handler(self, value):
    self.output_buffer.append(value)

    print("[%s] Outputting %s" % (self.address, value))

    if len(self.output_buffer) == 3:
      dest = self.output_buffer.pop(0)
      x = self.output_buffer.pop(0)
      y = self.output_buffer.pop(0)

      if dest == 255:
        print("[%s] Sending %s, %s" % (self.address, x, y))
        sys.exit(0)

      self.nics[dest].receive(x, y)

      print("[%s] Sending %s, %s to %s" % (self.address, x, y, dest))
      self.output_buffer.clear()

  def boot(self, nics):
    self.nics = nics

    self.computer.output_handler = self.output_handler
    self.computer.input(self.address)
    self.computer.run_program()

  def go(self):
    self.computer.execution_loop()

  def receive(self, x, y):
    print("[%s] Receiving [%s,%s]" % (self.address, x, y))
    self.computer.input(x, y)


def part1():
  program = [int(value) for value in open('day23/input.txt').readlines()[0].strip().split(",")]
  nics = [NIC(i, program) for i in range(0, 50)]
  #
  # for nic in nics:
  # def boot_nic():
  #   print("Booting nic: %s " % nic.address)
  #   nic.boot(nics)
  #
  # Thread(target=boot_nic).start()

  for nic in nics:
    nic.boot(nics)

  for nic in nics:
    nic.go()
    if nic.computer.waiting_for_input:
      nic.computer.input(-1)


part1()
