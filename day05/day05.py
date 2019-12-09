import unittest

from day05.instruction_set import *

OP_HALT = 99
OP_MUL = 2
OP_ADD = 1
OP_IN = 3
OP_OUT = 4
OP_JUMP_IF_TRUE = 5
OP_JUMP_IF_FALSE = 6
OP_LT = 7
OP_EQ = 8


OP_CODES_LABELS = {
  99: 'EN',
  2: 'MU',
  1: 'AD',
  3: 'IN',
  4: 'OU',
  5: 'JT',
  6: 'JF',
  7: 'LT',
  8: 'EQ',
  9: 'AB',
}

OP_PARAM_COUNTS = {
  OP_HALT: 0,
  OP_MUL: 3,
  OP_ADD: 3,  # A + B -> C
  OP_IN: 1,
  OP_OUT: 1,
  OP_JUMP_IF_TRUE: 2,
  OP_JUMP_IF_FALSE: 2,
  OP_LT: 3,
  OP_EQ: 3,
  OpCodes.OP_ARB: 1,
}

# TODO Add output positions per OP_CODE
OP_OUTPUT_POSITIONS = {
  OP_HALT: [],  # 0,
  OP_MUL: [2],  # 3,
  OP_ADD: [2],  # 3,
  OP_IN: [0],  # 1,
  OP_OUT: [],  # 1,
  OP_JUMP_IF_TRUE: [],  # 2,
  OP_JUMP_IF_FALSE: [],  # 2,
  OP_LT: [2],  # 3,
  OP_EQ: [2],  # 3,
  OpCodes.OP_ARB: [],  # 1
}

MODE_POS = 0
MODE_IMM = 1

class IntCodeComputer:
  def __init__(self, name="Computer"):
    self.instruction_pointer = 0
    self.positions = [OP_HALT]
    self.inputs = []
    self.output = []
    self.debug = True
    self.linked_output_computer = None
    self.waiting_for_input = False
    self.name = name
    self.relative_base = 0

  def reset(self):
    self.instruction_pointer = 0
    self.positions = [OP_HALT]
    self.inputs = []
    self.output = []
    self.waiting_for_input = False
    self.relative_base = 0

  def load(self, input_program):
    self.reset()
    self.positions.clear()
    self.positions.extend(input_program)

  def read(self, position):
    if position >= len(self.positions):
      return 0
    else:
      return self.positions[position]

  def write(self, position, value):
    extra_memory = position - len(self.positions) + 1
    if extra_memory > 0:
      self.positions.extend([0] * extra_memory)
    self.positions[position] = value

  def get_parameters(self, instruction_pointer, modes, output_parameters=[]):
    parameters = []
    for (position_index, mode) in enumerate(modes):
      if mode == Modes.IMM or position_index in output_parameters:
        parameter = self.read(instruction_pointer + position_index + 1)
      elif mode == Modes.REL:
        relative_value = self.read(instruction_pointer + position_index + 1)
        parameter = self.read(self.relative_base + relative_value)
      else:
        parameter = self.read(self.read(instruction_pointer + position_index + 1))

      parameters.append(parameter)

    return parameters

  def parse_instruction(self, instruction):
    op_code = instruction % 100
    modes_value = instruction // 100

    first_mode = modes_value % 10

    modes_value = modes_value // 10
    second_mode = modes_value % 10

    modes_value = modes_value // 10
    third_mode = modes_value % 10

    mode_count = OP_PARAM_COUNTS[op_code]

    return (op_code, [first_mode, second_mode, third_mode][0:mode_count])

  def link_output(self, computer):
    self.linked_output_computer = computer

  def load_from_file(self, filename):
    program = [int(value) for value in open(filename).readlines()[0].strip().split(",")]
    self.load(program)

  def run_program(self, program=None, inputs=None):
    if program is not None:
      self.load(program)

    if inputs is not None:
      self.inputs = inputs

    if inputs is not None and None in inputs:
      raise ValueError("None in input! %s" % (inputs,))

    if self.debug:
      print(''.join([str(p).rjust(5, ' ') for p in range(0, len(self.positions))]))

    self.execution_loop()

  def execution_loop(self):
    while True:
      jump_override = False
      instruction = self.positions[self.instruction_pointer]

      (op_code, parameter_modes) = self.parse_instruction(instruction)
      if self.debug:
        print(''.join([(('%s%s' % (OP_CODES_LABELS[op_code], ''.join(
          '*' if m == 0 else '-' for m in parameter_modes))) if p == self.instruction_pointer else str(val)).rjust(5,
                                                                                                                   ' ')
                       for p, val in
                       enumerate(self.positions)]), end='')

        print('   %s / %s RB=%s' % (self.inputs, self.output, self.relative_base))

      parameter_count = len(parameter_modes)
      if op_code == OP_ADD:  # add A + B -> C
        (val_a, val_b, output_position) = self.get_parameters(self.instruction_pointer, parameter_modes,
                                                              OP_OUTPUT_POSITIONS[op_code])

        val_c = val_a + val_b
        self.write(output_position, val_c)
      elif op_code == OP_MUL:  # multiply A * B -> C
        (val_a, val_b, output_position) = self.get_parameters(self.instruction_pointer, parameter_modes,
                                                              OP_OUTPUT_POSITIONS[op_code])

        val_c = val_a * val_b
        self.write(output_position, val_c)
      elif op_code == OP_IN:
        if len(self.inputs) == 0:
          self.waiting_for_input = True
          print("[%s] waiting for input" % self.name)
          return
        else:
          _input = self.inputs.pop(0)

        if _input is None:
          raise ValueError("Input was NONE")

        (output_position,) = self.get_parameters(self.instruction_pointer, parameter_modes,
                                                 OP_OUTPUT_POSITIONS[op_code])

        # output_position = self.read(self.instruction_pointer + 1)
        self.write(output_position, _input)
      elif op_code == OP_OUT:
        (value,) = self.get_parameters(self.instruction_pointer, parameter_modes, OP_OUTPUT_POSITIONS[op_code])

        if self.linked_output_computer:
          print("[%s] passing output [%s] to linked computer" % (self.name, value))
          self.linked_output_computer.input(value)

        self.output.append(value)
      elif op_code == OP_JUMP_IF_TRUE:
        (val_a, jump_position) = self.get_parameters(self.instruction_pointer, parameter_modes,
                                                     OP_OUTPUT_POSITIONS[op_code])

        if val_a != 0:
          self.instruction_pointer = jump_position
          jump_override = True
      elif op_code == OP_JUMP_IF_FALSE:
        (val_a, jump_position) = self.get_parameters(self.instruction_pointer, parameter_modes,
                                                     OP_OUTPUT_POSITIONS[op_code])

        if val_a == 0:
          self.instruction_pointer = jump_position
          jump_override = True
      elif op_code == OP_EQ:
        (val_a, val_b, output_position) = self.get_parameters(self.instruction_pointer, parameter_modes,
                                                              OP_OUTPUT_POSITIONS[op_code])
        if (val_a == val_b):
          self.write(output_position, 1)
        else:
          self.write(output_position, 0)
      elif op_code == OP_LT:
        (val_a, val_b, output_position) = self.get_parameters(self.instruction_pointer, parameter_modes,
                                                              OP_OUTPUT_POSITIONS[op_code])

        self.write(output_position, 1 if val_a < val_b else 0)
      elif op_code == OP_HALT:
        break

      # TODO: Move OpCode logic to seperate methods
      elif op_code == OpCodes.OP_ARB:
        (val_a,) = self.get_parameters(self.instruction_pointer, parameter_modes, OP_OUTPUT_POSITIONS[op_code])

        self.relative_base += val_a
        pass
      if not jump_override:
        self.instruction_pointer += 1 + parameter_count
    if self.debug:
      print("")

  def input(self, value):
    self.inputs.append(value)
    if self.waiting_for_input:
      print("[%s] Input received  %s. continue execution" % (self.name, value))
      self.execution_loop()


class Day5Part1(IntCodeComputer):
  def solve(self, args):
    pass


class Day5Part2(IntCodeComputer):
  def solve(self, args):
    pass


class Examples(unittest.TestCase):
  def test_add_operation(self):
    instruction = InstructionSet.add(Modes.IMM, Modes.IMM, 0)
    self.assertEqual(1101, instruction)

  def test_mul_operation(self):
    instruction = InstructionSet.mul(Modes.POS, Modes.IMM, 7)
    self.assertEqual(71002, instruction)

  def test_add_position_mode(self):
    computer = IntCodeComputer()
    # 2 + 3 = 5
    computer.load([
      InstructionSet.add(Modes.POS, Modes.POS),  # 0 instruction
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
    computer.load([InstructionSet.add(Modes.IMM, Modes.IMM), 2, 3, 0, 99])
    computer.run_program()
    self.assertEqual(5, computer.positions[0])

  def test_instruction_jump(self):
    computer = IntCodeComputer()
    computer.run_program([OP_OUT, 7, OP_OUT, 7, OP_OUT, 7, OP_HALT, 42])
    self.assertEqual([42, 42, 42], computer.output)

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
    self.assertEqual([Modes.POS, Modes.IMM, Modes.POS], modes)

  def test_parse_mode_halt(self):
    computer = IntCodeComputer()
    (op_code, modes) = computer.parse_instruction(99)

    self.assertEqual(OP_HALT, op_code)
    self.assertEqual([], modes)

  def test_equals(self):
    computer = IntCodeComputer()
    computer.run_program([InstructionSet.eq(Modes.IMM, Modes.IMM), 1, 2, 0, 99])
    self.assertEqual(0, computer.positions[0])
    computer.run_program([InstructionSet.eq(Modes.IMM, Modes.IMM), 1, 1, 0, 99])
    self.assertEqual(1, computer.positions[0])

    computer.run_program([InstructionSet.eq(Modes.IMM, Modes.POS), 108, 0, 0, 99])
    self.assertEqual(1, computer.positions[0])

    computer.run_program([InstructionSet.eq(Modes.IMM, Modes.POS), 107, 0, 0, 99])
    self.assertEqual(0, computer.positions[0])

  def test_less_than(self):
    computer = IntCodeComputer()

    computer.run_program([InstructionSet.lt(Modes.IMM, Modes.IMM), 1, 2, 0, 99])
    self.assertEqual(1, computer.positions[0])

    computer.run_program([InstructionSet.lt(Modes.IMM, Modes.IMM), 2, 2, 0, 99])
    self.assertEqual(0, computer.positions[0])

    computer.run_program([InstructionSet.lt(Modes.IMM, Modes.IMM), 2, 0, 0, 99])
    self.assertEqual(0, computer.positions[0])

  def test_jump_if_true(self):
    computer = IntCodeComputer()

    computer.run_program([InstructionSet.jump_if_true(Modes.IMM), 0, 4, 99, InstructionSet.op_output(Modes.POS), 1, 99])
    self.assertEqual([], computer.output)

    computer.run_program(
      [InstructionSet.jump_if_true(Modes.IMM), 42, 4, 99, InstructionSet.op_output(Modes.POS), 1, 99])
    self.assertEqual([42], computer.output)

  def test_jump_if_false(self):
    computer = IntCodeComputer()

    computer.run_program(
      [InstructionSet.jump_if_false(Modes.IMM), 42, 4, 99, InstructionSet.op_output(Modes.POS), 3, 99])
    self.assertEqual([], computer.output)

    computer.run_program(
      [InstructionSet.jump_if_false(Modes.IMM), 0, 4, 99, InstructionSet.op_output(Modes.POS), 3, 99])
    self.assertEqual([99], computer.output)

  def test_part1_example_negative(self):
    computer = IntCodeComputer()
    computer.run_program([1101, 100, -1, 4, 0])
    self.assertEqual(99, computer.positions[4])

  def test_part2_example_compare_8(self):
    computer = IntCodeComputer()

    computer.run_program([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], inputs=[8])
    self.assertEqual([1], computer.output, "1. position mode: 8 == 8 -> 1")

    computer.run_program([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], inputs=[3])
    self.assertEqual([0], computer.output, "1. position mode: 3 == 8 -> 0")

    computer.run_program([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], inputs=[7])
    self.assertEqual([1], computer.output, "2. position mode: 7 < 8 -> 1")

    computer.run_program([3, 3, 1108, -1, 8, 3, 4, 3, 99], inputs=[8])
    self.assertEqual([1], computer.output, "3. immediate mode: 8 == 8 -> 1")

    computer.run_program([3, 3, 1107, -1, 8, 3, 4, 3, 99], inputs=[7])
    self.assertEqual([1], computer.output, "4. immediate mode: 7 < 8 -> 1")

  def test_part2_example_jump_tests(self):
    computer = IntCodeComputer()

    computer.run_program([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], inputs=[0])
    self.assertEqual([0], computer.output, "position mode 0 == 0 -> 0")

    computer.run_program([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], inputs=[7])
    self.assertEqual([1], computer.output, "position mode 7 != 0 -> 1")

    computer.run_program([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], inputs=[0])
    self.assertEqual([0], computer.output, "immediate mode 0 == 0 -> 0")

    computer.run_program([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], inputs=[7])
    self.assertEqual([1], computer.output, "immediate mode 7 != 0 -> 1")

  def test_part2_example_larger_jump_test(self):
    computer = IntCodeComputer()
    computer.load([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                   1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                   999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99])

    computer.run_program(inputs=[7])
    self.assertEqual([999], computer.output, "return 999 if 7 < 8")

class Solutions(unittest.TestCase):
  def test_part1(self):
    with open("day05/input.txt") as fh:
      computer = IntCodeComputer()
      computer.load([int(value) for value in fh.readlines()[0].strip().split(",")])
      computer.input(1)
      computer.run_program()
      print(computer.output)
      # 45074395 Correct

  def test_part2(self):
    with open("day05/input.txt") as fh:
      computer = IntCodeComputer()
      computer.load([int(value) for value in fh.readlines()[0].strip().split(",")])
      computer.input(5)
      computer.run_program()
      print(computer.output)
      # 8346937 Correct
