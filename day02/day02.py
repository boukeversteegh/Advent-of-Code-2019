# Op codes
# 1 ADD A B -> C
# 2 MULT A B -> C
#
# 99 HALT
#
# +4


input_program = [int(code) for code in open("input.txt")
  .readlines()[0].strip().split(',')]


def reset():
  global positions
  positions = input_program
  positions[1] = 12
  positions[2] = 2


reset()

# Example
# P0 = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
P1 = [1, 0, 0, 0, 99]
P2 = [2, 3, 0, 3, 99]
P3 = [2, 4, 4, 5, 99, 0]
P4 = [1, 1, 1, 4, 99, 5, 6, 0, 99]

# positions

instruction_pointer = 0


def get_parameters(position):
  global arg_c, val_a, val_b
  arg_a = position + 1
  arg_b = position + 2
  arg_c = position + 3
  pos_a = positions[arg_a]
  pos_b = positions[arg_b]
  pos_c = positions[arg_c]

  val_a = positions[pos_a]
  val_b = positions[pos_b]
  print("OP A=%s B=%s -> C=%s" % (arg_a, arg_b, pos_c))
  return val_a, val_b, pos_c


def print_positions(in_positions):
  print(",".join([str(code) for code in in_positions]))


print_positions(positions)

while True:
  opcode = positions[instruction_pointer]

  if opcode == 1:
    # add A + B -> C
    (val_a, val_b, arg_c) = get_parameters(instruction_pointer)

    val_c = val_a + val_b
    positions[arg_c] = val_c
    instruction_pointer += 4

  if opcode == 2:
    # multiply A * B -> C
    (val_a, val_b, arg_c) = get_parameters(instruction_pointer)

    val_c = val_a * val_b
    positions[arg_c] = val_c
    instruction_pointer += 4

  if opcode == 99:
    # instruction_pointer += 1
    break

  print_positions(positions)

print_positions(positions)
