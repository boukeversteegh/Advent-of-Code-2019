from day07.day07 import AmpRunner
from day09.day09 import IntCodeComputerDay9

computer = IntCodeComputerDay9()

program = AmpRunner.load_program_from_file('day19/input.txt')
computer.debug = False

yes = 0
inputs = []
for y in range(0, 50):
  for x in range(0, 50):
    computer.run_program(program=program, inputs=[x, y])
    in_beam = computer.output[0]
    if in_beam == 1:
      yes += 1
    print("#" if in_beam else '.', end='')
  print()
  # breakpoint()

print(yes)
