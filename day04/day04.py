import unittest


class PasswordSolver:
  def __init__(self):
    pass

  def count_valid_passwords(self):
    valid_count = 0
    for password in range(240298, 784956 + 1):
      if self.is_valid(str(password)):
        valid_count += 1

    return valid_count


class PasswordSolverPart1(PasswordSolver):
  def is_valid(self, password):
    password = str(password)
    if len(password) != 6:
      return False

    have_double = False
    is_monotonous = True
    current_sequence = ''
    sequence_length = 0

    for p in range(0, 6):
      digit = password[p]

      if digit != current_sequence:
        if sequence_length >= 2:
          have_double = True

        current_sequence = digit
        sequence_length = 1
      else:
        sequence_length += 1

      if p < 5 and digit > password[p + 1]:
        is_monotonous = False

    if sequence_length >= 2:
      have_double = True

    if not have_double:
      return False

    if not is_monotonous:
      return False

    return True


class PasswordSolverPart2(PasswordSolver):
  def is_valid(self, password):
    password = str(password)
    if len(password) != 6:
      return False

    have_double = False
    is_monotonous = True
    current_sequence = ''
    sequence_length = 0

    for p in range(0, 6):
      digit = password[p]

      if digit != current_sequence:
        if sequence_length == 2:
          have_double = True

        current_sequence = digit
        sequence_length = 1
      else:
        sequence_length += 1

      if p < 5 and digit > password[p + 1]:
        is_monotonous = False

    if sequence_length == 2:
      have_double = True

    if not have_double:
      return False

    if not is_monotonous:
      return False

    return True


class Examples(unittest.TestCase):
  def test_examples_part1(self):
    self.day4 = PasswordSolverPart1()
    self.assertTrue(self.day4.is_valid('111111'))
    self.assertTrue(self.day4.is_valid('456779'))
    self.assertTrue(self.day4.is_valid('000000'))
    self.assertFalse(self.day4.is_valid('223450'))
    self.assertFalse(self.day4.is_valid(''))
    self.assertFalse(self.day4.is_valid('123'))
    self.assertFalse(self.day4.is_valid('12345'))
    self.assertFalse(self.day4.is_valid('1234567'))
    self.assertFalse(self.day4.is_valid('123789'))
    self.assertFalse(self.day4.is_valid('338879'))

  def test_examples_part2A(self):
    self.day4 = PasswordSolverPart2()
    self.assertFalse(self.day4.is_valid('111111'))
    self.assertTrue(self.day4.is_valid('456779'))
    self.assertFalse(self.day4.is_valid('000000'))
    self.assertFalse(self.day4.is_valid('223450'))
    self.assertFalse(self.day4.is_valid(''))
    self.assertFalse(self.day4.is_valid('123'))
    self.assertFalse(self.day4.is_valid('12345'))
    self.assertFalse(self.day4.is_valid('1234567'))
    self.assertFalse(self.day4.is_valid('123789'))
    self.assertFalse(self.day4.is_valid('338879'))

  def test_examples_part2B(self):
    self.day4 = PasswordSolverPart2()
    valid = [
      '112233',
      '111122',
      '334566',
    ]
    invalid = [
      '111111',
      '123444',
      '444567',
      '000123',
    ]
    for v in valid:
      self.assertTrue(self.day4.is_valid(v), msg="%s should be valid" % v)

    for i in invalid:
      self.assertFalse(self.day4.is_valid(i), msg="%s should be INVALID" % v)


class Solutions(unittest.TestCase):
  def test_part1(self):
    day4 = PasswordSolverPart1()
    valid_count = day4.count_valid_passwords()
    print(valid_count)

  def test_part2(self):
    day4 = PasswordSolverPart2()
    valid_count = day4.count_valid_passwords()
    print(valid_count)


# Part 1 1150
# Part 2 648 BAD
# Part 2 454 BAD
# Part 2 510 BAD
# Part 2 748
