import unittest

OP_HALT = 99
OP_MUL = 2
OP_ADD = 1
OP_IN = 3
OP_OUT = 4

OP_PARAM_COUNTS = {
  OP_HALT: 0,
  OP_MUL: 3,
  OP_ADD: 3,  # A + B -> C
  OP_IN: 1,
  OP_OUT: 1,
}

MODE_POS = 0
MODE_IMM = 1


class IntCodeComputer:
  def __init__(self):
    self.instruction_pointer = 0
    self.positions = [OP_HALT]
    self._input = None
    self.output = None

  def reset(self):
    self.instruction_pointer = 0
    self.positions = [OP_HALT]
    self._input = None
    self.output = None

  def load(self, input_program):
    self.positions.clear()
    self.positions.extend(input_program)

  def get_parameters(self, position, nr):
    pos_a = self.positions[position + 1]
    pos_b = self.positions[position + 2]
    if nr == 3:
      pos_c = self.positions[position + 3]

    val_a = self.positions[pos_a]
    val_b = self.positions[pos_b]
    if nr == 3:
      return val_a, val_b, pos_c

    if nr == 1:
      return val_a

  def parse_instruction(self, instruction):
    op_code = instruction % 100
    modes_value = int(instruction / 100)

    first_mode = modes_value % 10

    modes_value = int(modes_value / 10)
    second_mode = modes_value % 10

    modes_value = int(modes_value / 10)
    third_mode = modes_value % 10

    mode_count = OP_PARAM_COUNTS[op_code]

    return (op_code, [first_mode, second_mode, third_mode][0:mode_count])

  def run_program(self):
    if self.positions[0] not in [OP_ADD, OP_MUL, OP_HALT]:
      raise Exception("Program does not start with instruction: %s" % self.positions)

    while True:
      instructions = self.positions[self.instruction_pointer]
      (op_code, parameter_modes) = self.parse_instruction(instructions)

      if op_code == OP_ADD:  # add A + B -> C
        (val_a, val_b, arg_c) = self.get_parameters(self.instruction_pointer)

        val_c = val_a + val_b
        self.positions[arg_c] = val_c

      elif op_code == OP_MUL:  # multiply A * B -> C
        (val_a, val_b, arg_c) = self.get_parameters(self.instruction_pointer)

        val_c = val_a * val_b
        self.positions[arg_c] = val_c

      elif op_code == OP_HALT:
        break

      self.instruction_pointer += 4

      print(self.instruction_pointer)

  def write(self, position, value):
    self.positions[position] = value

  def result(self):
    return self.positions[0]

  def input(self, value):
    self._input = value


class Day5Part1(IntCodeComputer):
  def solve(self, args):
    pass


class Day5Part2(IntCodeComputer):
  def solve(self, args):
    pass


def add(first_mode, second_mode, output_mode=MODE_POS):
  return OP_ADD + 100 * first_mode + 1000 * second_mode + 10000 * output_mode


def mul(first_mode, second_mode, output_mode=MODE_POS):
  return OP_MUL + 100 * first_mode + 1000 * second_mode + 10000 * output_mode


def op_input(output_position):
  return OP_IN * 100 + 1000 * output_position

class Examples(unittest.TestCase):
  def test_add_operation(self):
    instruction = add(MODE_IMM, MODE_IMM, 0)
    self.assertEqual(1101, instruction)

  def test_mul_operation(self):
    instruction = mul(MODE_POS, MODE_IMM, 7)
    self.assertEqual(71002, instruction)

  def test_add_immediate_mode(self):
    computer = IntCodeComputer()
    # 2 + 3 = 5
    computer.load([add(MODE_IMM, MODE_IMM), 2, 3, 0])
    self.assertEqual(5, computer.positions[0])

  def test_identity(self):
    computer = IntCodeComputer()
    computer.load([3, 0, 4, 0, 99])
    computer.input(33)
    self.assertEqual([33], computer.output)

  def test_parse_mode_add(self):
    computer = IntCodeComputer()
    (op_code, modes) = computer.parse_instruction(1002)

    self.assertEqual(OP_MUL, op_code)
    self.assertEqual([MODE_POS, MODE_IMM, MODE_POS], modes)

  def test_parse_mode_halt(self):
    computer = IntCodeComputer()
    (op_code, modes) = computer.parse_instruction(99)

    self.assertEqual(OP_HALT, op_code)
    self.assertEqual([], modes)


class Solutions(unittest.TestCase):
  def test_part1(self):
    day5 = Day5Part1()

  def test_part2(self):
    day5 = Day5Part2()
