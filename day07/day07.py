import unittest
from itertools import permutations

from day05.day05 import IntCodeComputer, Examples


class IntCodeComputerDay7(IntCodeComputer):
  def __init__(self):
    super().__init__()

  def load_from_file(self, filename):
    program = [int(value) for value in open(filename).readlines()[0].strip().split(",")]
    self.load(program)


class AmpRunner:
  @staticmethod
  def load_program_from_file(filename):
    return [int(value) for value in open(filename).readlines()[0].strip().split(",")]

  @staticmethod
  def run_amps(amps, phase_settings, program):
    amps_inputs = [
      [phase_settings[0], 0],
      [phase_settings[1], None],
      [phase_settings[2], None],
      [phase_settings[3], None],
      [phase_settings[4], None]
    ]
    for i, (amp, inputs) in enumerate(zip(amps, amps_inputs)):
      print("Running amp %s with settings: %s" % (i, inputs))
      amp.run_program(program=program, inputs=inputs)

      print(amp.output)
      amp_output = amp.output[0]
      if i < 4:
        amps_inputs[i + 1][1] = amp_output
      else:
        return amp_output


class Examples(Examples):
  def test_part1_1(self):
    amps = [
      IntCodeComputerDay7(),
      IntCodeComputerDay7(),
      IntCodeComputerDay7(),
      IntCodeComputerDay7(),
      IntCodeComputerDay7(),
    ]

    for amp in amps:
      amp.load(input_program=[3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0])

    self.assertEqual(43210, AmpRunner.run_amps(amps, [4, 3, 2, 1, 0]))



class Solutions(unittest.TestCase):

  def test_part1(self):
    amps = [
      IntCodeComputerDay7(),
      IntCodeComputerDay7(),
      IntCodeComputerDay7(),
      IntCodeComputerDay7(),
      IntCodeComputerDay7(),
    ]

    program = AmpRunner.load_program_from_file("input.txt")
    for amp in amps:
      amp.debug = False

    scores = [(setting, AmpRunner.run_amps(amps, setting, program)) for setting in permutations([0, 1, 2, 3, 4])]

    for score in scores:
      print(score)
    print(max(scores, key=lambda score: score[1]))

    # 40708 BAD

  # def test_part2(self):
  #   solution = Day7()

# input 0-4
