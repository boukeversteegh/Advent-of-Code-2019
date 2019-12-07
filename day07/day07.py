import unittest
from itertools import permutations

from day05.constants import OpCodes
from day05.day05 import IntCodeComputer, MODE_POS, MODE_IMM
from day05.instruction_set import InstructionSet


class IntCodeComputerDay7(IntCodeComputer):
  def link_output(self, computer):
    self.linked_output_computer = computer

  def load_from_file(self, filename):
    program = [int(value) for value in open(filename).readlines()[0].strip().split(",")]
    self.load(program)

class AmpRunner:
  @staticmethod
  def load_program_from_file(filename):
    return [int(value) for value in open(filename).readlines()[0].strip().split(",")]

  @staticmethod
  def run_amps_in_loop(amps, phase_settings, program):
    for index, amp in enumerate(amps):
      amp.load(program)
      amp.input(phase_settings[index])

    amps[0].input(0)

    for i, amp in enumerate(amps):
      print("Running amp %s with settings: %s" % (i, phase_settings))
      amp.run_program()

    return amps[-1].output[-1]

  @staticmethod
  def run_amps_in_sequence(amps, phase_settings, program):
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


class ExamplesDay7(unittest.TestCase):

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

    self.assertEqual(43210, AmpRunner.run_amps_in_sequence(amps, [4, 3, 2, 1, 0], program=None))

  def test_wait_for_input(self):
    computer = IntCodeComputerDay7()
    computer.load([InstructionSet.op_input(), 5, InstructionSet.op_output(MODE_POS), 5, OpCodes.OP_HALT, 0])

    computer.run_program()
    computer.input(42)

    self.assertEqual([42], computer.output)

  def test_linking_computers(self):
    first = IntCodeComputerDay7()
    second = IntCodeComputerDay7()

    first.link_output(second)

    first.load([InstructionSet.op_output(MODE_IMM), 42, OpCodes.OP_HALT])
    second.load([InstructionSet.op_input(), 7, InstructionSet.op_output(MODE_POS), 7, 99, 0, 0, 0])

    print("Run Second")
    second.run_program(inputs=[42])

    print("Run First")
    first.run_program()

    self.assertEqual([42], second.output)

class Solutions(unittest.TestCase):
  def test_part1(self):
    amps = [
      IntCodeComputerDay7(),
      IntCodeComputerDay7(),
      IntCodeComputerDay7(),
      IntCodeComputerDay7(),
      IntCodeComputerDay7(),
    ]

    program = AmpRunner.load_program_from_file("day07/input.txt")
    for amp in amps:
      amp.debug = False

    scores = [(setting, AmpRunner.run_amps_in_sequence(amps, setting, program)) for setting in
              permutations([0, 1, 2, 3, 4])]

    print(max(scores, key=lambda score: score[1]))

    # 40708 BAD
    # 46248 GOOD

  def test_part2(self):
    amps = [
      IntCodeComputerDay7("amp-0"),
      IntCodeComputerDay7("amp-1"),
      IntCodeComputerDay7("amp-2"),
      IntCodeComputerDay7("amp-3"),
      IntCodeComputerDay7("amp-4"),
    ]

    program = AmpRunner.load_program_from_file("day07/input.txt")
    for amp_index, amp in enumerate(amps):
      amp.debug = False
      if amp_index < len(amps) - 1:
        amp.link_output(amps[amp_index + 1])

    amps[-1].link_output(amps[0])

    scores = [(setting, AmpRunner.run_amps_in_loop(amps, setting, program)) for setting in
              permutations([5, 6, 7, 8, 9])]

    print(max(scores, key=lambda score: score[1]))
    # 54163586
