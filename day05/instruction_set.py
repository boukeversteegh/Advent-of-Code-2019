# OpCodes = constants.OpCodes
# Modes = constants.Modes
from day05.constants import Modes, OpCodes


class InstructionSet:
  @staticmethod
  def add(first_mode, second_mode, output_mode=Modes.POS):
    return OpCodes.OP_ADD + 100 * first_mode + 1000 * second_mode + 10000 * output_mode

  @staticmethod
  def mul(first_mode, second_mode, output_mode=Modes.POS):
    return OpCodes.OP_MUL + 100 * first_mode + 1000 * second_mode + 10000 * output_mode

  @staticmethod
  def eq(first_mode, second_mode):
    return OpCodes.OP_EQ + 100 * first_mode + 1000 * second_mode + 10000 * Modes.POS

  @staticmethod
  def lt(first_mode, second_mode):
    return OpCodes.OP_LT + 100 * first_mode + 1000 * second_mode + 10000 * Modes.POS

  @staticmethod
  def op_input():
    return OpCodes.OP_IN

  @staticmethod
  def jump_if_true(first_mode):
    return OpCodes.OP_JUMP_IF_TRUE + 100 * first_mode

  @staticmethod
  def jump_if_false(first_mode):
    return OpCodes.OP_JUMP_IF_FALSE + 100 * first_mode

  @staticmethod
  def op_output(first_mode):
    return OpCodes.OP_OUT + 100 * first_mode
