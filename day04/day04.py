import unittest


class Day4:
  def __init__(self):
    pass

  def part1(self):
    valid_count = 0
    for password in range(240298, 784956 + 1):
      if self.is_valid(str(password)):
        valid_count += 1

    return valid_count

  def is_valid(self, password):
    if len(password) != 6:
      return False

    have_double = False
    is_monotonous = True
    for p in range(0, 5):

      if password[p] == password[p + 1]:
        have_double = True

      if password[p] > password[p + 1]:
        is_monotonous = False

    if not have_double:
      return False

    if not is_monotonous:
      return False

    return True


class Tests(unittest.TestCase):

  def __init__(self, methodName: str = ...) -> None:
    super().__init__(methodName)
    self.day4 = Day4()

  def test_examples(self):
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

  def test_part1(self):
    day4 = Day4()
    valid_count = day4.part1()
    print(valid_count)


def main():
  day4 = Day4()
  valid_count = day4.part1()
  print(valid_count)


if __name__ == '__main__':
  main()
