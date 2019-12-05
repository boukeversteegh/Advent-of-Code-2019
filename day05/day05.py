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
    self.inputs = []
    self.output = []

  def reset(self):
    self.instruction_pointer = 0
    self.positions = [OP_HALT]
    self.inputs = []
    self.output = []

  def load(self, input_program):
    self.positions.clear()
    self.positions.extend(input_program)

  def get_parameters(self, instruction_pointer, modes):
    parameters = []
    for (position_index, mode) in enumerate(modes):
      if mode == MODE_IMM:
        parameter = self.positions[instruction_pointer + position_index + 1]
      else:
        parameter = self.positions[self.positions[instruction_pointer + position_index + 1]]

      parameters.append(parameter)

    return parameters


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
    while True:
      instruction = self.positions[self.instruction_pointer]
      (op_code, parameter_modes) = self.parse_instruction(instruction)

      parameter_count = len(parameter_modes)

      if op_code == OP_ADD:  # add A + B -> C
        (val_a, val_b, arg_c) = self.get_parameters(self.instruction_pointer, parameter_modes)

        output_position = self.positions[self.instruction_pointer + 3]

        val_c = val_a + val_b
        self.positions[output_position] = val_c

      elif op_code == OP_MUL:  # multiply A * B -> C
        (val_a, val_b, arg_c) = self.get_parameters(self.instruction_pointer, parameter_modes)

        output_position = self.positions[self.instruction_pointer + 3]

        val_c = val_a * val_b
        self.positions[output_position] = val_c

      elif op_code == OP_IN:
        _input = self.inputs.pop(0)
        if _input is None:
          raise ValueError("No more input!")

        output_position = self.positions[self.instruction_pointer + 1]
        self.positions[output_position] = _input
      elif op_code == OP_OUT:
        value = self.positions[self.positions[self.instruction_pointer + 1]]
        self.output.append(value)

      elif op_code == OP_HALT:
        break

      self.instruction_pointer += 1 + parameter_count

      print(self.instruction_pointer)

  def write(self, position, value):
    self.positions[position] = value

  def result(self):
    return self.positions[0]

  def input(self, value):
    self.inputs.append(value)


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

  def test_add_position_mode(self):
    computer = IntCodeComputer()
    # 2 + 3 = 5
    computer.load([
      add(MODE_POS, MODE_POS),  # 0 instruction
      5,  # 1: arg 1
      6,  # 2: arg 2
      0,  # 3: arg 3,
      99,  # 4: halt
      2,  # 5: arg 1 value
      3,  # 6: arg 2 value,
    ])
    computer.run_program()
    self.assertEqual(5, computer.positions[0])

  def test_add_immediate_mode(self):
    computer = IntCodeComputer()
    # 2 + 3 = 5
    computer.load([add(MODE_IMM, MODE_IMM), 2, 3, 0, 99])
    computer.run_program()
    self.assertEqual(5, computer.positions[0])

  def test_input(self):
    computer = IntCodeComputer()
    computer.load([OP_IN, 0, 99, 99, 99])
    computer.input(33)
    computer.run_program()
    self.assertEqual(33, computer.positions[0])

  def test_output(self):
    computer = IntCodeComputer()
    computer.load([OP_OUT, 6, 99, 99, 99, 99, 42])
    computer.run_program()
    self.assertEqual([42], computer.output)

  def test_identity(self):
    computer = IntCodeComputer()
    computer.load([OP_IN, 0, OP_OUT, 0, 99])
    computer.input(33)
    computer.run_program()
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
