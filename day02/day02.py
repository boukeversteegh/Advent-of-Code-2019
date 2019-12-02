# Op codes
# 1 ADD A B -> C
# 2 MULT A B -> C
#
# 99 HALT
#
# +4

OP_HALT = 99
OP_MUL = 2
OP_ADD = 1

input_program = [int(code) for code in open("input.txt")
  .readlines()[0].strip().split(',')]

# Example
# P0 = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
P1 = [1, 0, 0, 0, 99]
P2 = [2, 3, 0, 3, 99]
P3 = [2, 4, 4, 5, 99, 0]
P4 = [1, 1, 1, 4, 99, 5, 6, 0, 99]

def print_positions(in_positions):
  print(",".join([str(code) for code in in_positions]))


class IntCodeComputer:
  def __init__(self):
    self.instruction_pointer = 0
    self.positions = [OP_HALT]
    self.reset()

  def reset(self):
    self.instruction_pointer = 0
    self.positions = [OP_HALT]

  def load(self, input_program):
    self.positions.clear()
    self.positions.extend(input_program)

  def get_parameters(self, position):
    pos_a = self.positions[position + 1]
    pos_b = self.positions[position + 2]
    pos_c = self.positions[position + 3]

    val_a = self.positions[pos_a]
    val_b = self.positions[pos_b]
    return val_a, val_b, pos_c

  def run_program(self):
    if self.positions[0] not in [OP_ADD, OP_MUL, OP_HALT]:
      raise Exception("Program does not start with instruction: %s" % self.positions)

    while True:
      op_code = self.positions[self.instruction_pointer]

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


target_output = 19690720

def part2():
  computer = IntCodeComputer()
  for noun in range(0, 100):
    for verb in range(0, 100):
      computer.reset()
      computer.load(input_program)
      computer.write(1, noun)
      computer.write(2, verb)

      print_positions(computer.positions)

      computer.run_program()

      result = computer.result()

      # print("VERB: %s/100" % verb)

      if result == target_output:
        print("NOUN=%s, VERB=%s, Answer: %s" % (noun, verb, 100 * noun + verb))
        return
    # print("NOUN: %s/100" % noun)

  print_positions(computer.positions)


part2()