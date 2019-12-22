import re

with open('day22/input.txt') as fh:
  lines = [line.strip() for line in fh.readlines()]

  deck_size = 10007
  # deck_size = 10

  table = list(range(0, deck_size))

  r_last_digits = r'(-?\d+)$'
  increment = None
  print(table)
  for line in lines:
    if line.startswith('deal with increment'):
      increment = int(re.search(r_last_digits, line).group(0))
      print("increment: %s" % increment)

      new_table = [None] * deck_size
      for old_position in range(0, deck_size):
        new_position = (old_position * increment) % deck_size
        new_table[new_position] = table[old_position]
      table = new_table
      print(table)

    if line == 'deal into new stack':
      print("Dealing into new stack")
      table = list(reversed(table))

    if line.startswith('cut'):
      cut_offset = int(re.search(r_last_digits, line).group(0))
      print('cut by %s' % cut_offset)
      if cut_offset < 0:
        cut_offset = deck_size + cut_offset
      print(' --> cut by %s' % cut_offset)
      table = table[cut_offset:] + table[:cut_offset]
      print(table)

  print(table)

  print(table.index(2019))
