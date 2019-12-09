import unittest

from day07.day07 import IntCodeComputerDay7


class IntCodeComputerDay9(IntCodeComputerDay7):

  def __init__(self, name="Computer"):
    super().__init__(name)


class Examples(unittest.TestCase):
  def test_part1_rb0(self):
    computer = IntCodeComputerDay9()

    computer.run_program([
      InstructionSet.op_output(Modes.POS),
      3,
      InstructionSet.halt(),
      42
    ])

    self.assertEqual([42], computer.output)

  def test_part1_adjust_relative_base(self):
    computer = IntCodeComputerDay9()

    computer.run_program([
      InstructionSet.adjust_relative_base(Modes.IMM),
      1,
      InstructionSet.op_output(Modes.REL),
      4,
      InstructionSet.halt(),
      42
    ])

    self.assertEqual([42], computer.output)

  def test_part1_relative_base_read(self):
    computer = IntCodeComputerDay9()

    computer.load([
      InstructionSet.op_output(Modes.REL),
      2,
      InstructionSet.halt(),
      42
    ])
    computer.relative_base = 1
    computer.run_program()

    self.assertEqual([42], computer.output)

  def test_part1_read_from_unallocated_memory(self):
    computer = IntCodeComputerDay9()

    computer.run_program([
      InstructionSet.op_output(Modes.POS),
      500,
      InstructionSet.halt()
    ])

    self.assertEqual([0], computer.output)

  def test_part1_write_and_read_unallocated_memory(self):
    computer = IntCodeComputerDay9()

    computer.run_program([
      InstructionSet.op_input(),
      500,
      InstructionSet.op_output(Modes.POS),
      500,
      InstructionSet.halt()
    ], inputs=[42])

    self.assertEqual([42], computer.output)

  def test_part1_add_to_unallocated_memory(self):
    computer = IntCodeComputerDay9()

    computer.run_program([
      InstructionSet.add(Modes.IMM, Modes.POS),
      42,
      500,
      501,
      InstructionSet.op_output(Modes.POS),
      501,
      InstructionSet.halt()
    ], inputs=[42])

    self.assertEqual([42], computer.output)

  def test_part1_examples(self):
    computer = IntCodeComputerDay9()

    program1 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    computer.run_program(program1)
    self.assertEqual(program1, computer.output)

  def test_part1_examples_large_int(self):
    computer = IntCodeComputerDay9()
    computer.run_program([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    self.assertEqual([1219070632396864], computer.output)

  def test_part2(self):
    pass


class Solutions(unittest.TestCase):
  def test_part1(self):
    computer = IntCodeComputerDay9()

    computer.load_from_file("day09/input.txt")
    computer.input(1)
    computer.run_program()

    print(computer.output)
    # 3409270027

  def test_part2(self):
    computer = IntCodeComputerDay9()
    computer.debug = False
    computer.load_from_file("day09/input.txt")
    computer.input(2)
    computer.run_program()
    print(computer.output)
    # 82760
