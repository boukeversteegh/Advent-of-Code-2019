import re

with open('day22/input.txt') as fh:
  lines = [line.strip() for line in fh.readlines()]

  deck_size = 10007
  # deck_size = 10

  # part 2
  deck_size = 119315717514047

  r_last_digits = r'(-?\d+)$'


  def log(*largs):
    # print(*largs)
    pass


  def part1():
    table = list(range(0, deck_size))
    increment = None
    log(table)
    for line in lines:
      if line.startswith('deal with increment'):
        increment = int(re.search(r_last_digits, line).group(0))
        log("increment: %s" % increment)

        new_table = [None] * deck_size
        for old_position in range(0, deck_size):
          new_position = (old_position * increment) % deck_size
          new_table[new_position] = table[old_position]
        table = new_table
        log(table)

      if line == 'deal into new stack':
        log("Dealing into new stack")
        table = list(reversed(table))

      if line.startswith('cut'):
        cut_offset = int(re.search(r_last_digits, line).group(0))
        log('cut by %s' % cut_offset)
        if cut_offset < 0:
          cut_offset = deck_size + cut_offset
        log(' --> cut by %s' % cut_offset)
        table = table[cut_offset:] + table[:cut_offset]
        log(table)

    log("Sorted:")
    log(table)


  # part1()

  def reverse_operation(line, sorted_position, deck_size):
    original_position = sorted_position
    log("[%s]" % sorted_position)
    if line.startswith('deal with increment'):
      increment = int(re.search(r_last_digits, line).group(0))
      log("- reverse increment: %s" % increment)

      # reverse increment operation
      factor = 0
      while (original_position + deck_size * factor) % increment:
        factor += 1

      original_position = (original_position + deck_size * factor) // increment
      log('   %s' % original_position)
      return original_position

    if line == 'deal into new stack':
      log("- reverse dealing into new stack")
      original_position = deck_size - original_position - 1
      log('   %s' % original_position)
      return original_position
      # table = list(reversed(table))

    if line.startswith('cut'):
      cut_offset = int(re.search(r_last_digits, line).group(0))
      log('- reverse cut by %s' % cut_offset)
      if cut_offset < 0:
        cut_offset = deck_size + cut_offset
      log(' --> reversed negative cut into %s' % cut_offset)

      reversed_cut_offset = deck_size - cut_offset

      log(' --> opposite cut offset is %s' % reversed_cut_offset)

      if original_position <= reversed_cut_offset:
        original_position = (original_position + cut_offset) % deck_size
        log('   %s' % original_position)
        return original_position
      else:
        original_position = original_position - reversed_cut_offset
        log('   %s' % original_position)
        return original_position
      # if reversed_cut_offset <= original_position:
      #   return original_position - cut_offset
      # if reversed_cut_offset > original_position:
      #   return original_position + cut_offset + 1


  # 1a [0, 3, 6, 9, 2, 5, 8, 1, [4], 7]
  # 1b [[3], 0, 7, 4, 1, 8, 5, 2, 9, 6]

  # R  [3, 10, 7, 4, 1, 8, 5, 2, 9, 6]
  def part2(sorted_position, deck_size, repeat=1):

    original_position = sorted_position
    # table = range(0, deck_size)

    positions = set()

    pattern_size = None
    for i in range(0, repeat):
      if i % 1000 == 0:
        print('%s' % i)
        # sys.stdout.write('%s\r' % i)
        # sys.stdout.flush()

      for line in reversed(lines):
        # print(original_position, end='')
        original_position = reverse_operation(line, original_position, deck_size)
        # print('\t', original_position)

        # table = [
        #   reverse_operation(line, p) for p in table
        # ]

        # log("Restored:", table)

      # print("Position: %s" % original_position)

      if pattern_size is None and original_position in positions:
        print("Pattern length is", i)
        pattern_size = i
        breakpoint()

      positions.add(original_position)

      if pattern_size is not None:
        if (i + 1) % pattern_size == (repeat % pattern_size):
          print("The original card's position was: %s" % original_position)
          return

    print()
    print("The original card's position was: %s" % original_position)
    # log(table.index(2019))


  # part2(2020, deck_size, 101741582076661 % 4)
  # part2(2020, deck_size, 101741582076661)

  for i in range(0, 100):
    p = i
    for line in reversed(lines):
      p = reverse_operation(line, p, deck_size)

    print("%s %s" % (i, p))
  # 13717216414483 too low
