import collections
from math import ceil


def parse_ingredient():
  rh_count, rh_el = rh.split(' ')
  rh_count = int(rh_count)


def parse_ingredient(s):
  count, el = s.split(' ')
  count = int(count)
  return count, el


reactions = {}

for line in open('day14/input.txt').readlines():
  lh, rh = line.strip().split(' => ')
  lh_ingredients = lh.split(', ')

  output_count, output_element = parse_ingredient(rh)

  input_ingredients = [parse_ingredient(ing) for ing in lh_ingredients]

  reactions[output_element] = (output_count, input_ingredients)
  # print(input_ingredients, output_ingredient)

# needed = [(1, 'FUEL')]
needed = collections.defaultdict(lambda: 0)
needed['FUEL'] = 1
needed_elements = []
needed_elements.append('FUEL')

available = collections.defaultdict(lambda: 0)
# available['ORE'] = 1000000000000

needed_ore = 0
while needed_elements:
  needed_el = needed_elements.pop(0)
  needed_count = needed[needed_el]
  if needed_el not in reactions:
    continue
  output_count, input_ingredients = reactions[needed_el]

  # need 3
  # have 2
  available_count = available[needed_el]
  using_count = min(available_count, needed_count)
  still_needed_count = needed_count - using_count
  available[needed_el] = available_count - using_count

  if still_needed_count > 0:
    reaction_count = ceil(still_needed_count / output_count)
    production_count = reaction_count * output_count
    left_over_production_count = production_count - still_needed_count
    available[needed_el] += left_over_production_count

    # print("Running reaction %s => %s", (input_ingredients, output_element))
    for needed_input_count, input_el in input_ingredients:
      # needed_el = 3
      # output_count = 2
      needed_input_count *= reaction_count
      print("For %s we need: %s %s" % (needed_el, needed_input_count, input_el))
      """
      For FUEL we need: 2 AB
For FUEL we need: 3 BC
For FUEL we need: 4 CA
For AB we need: 6 A
For AB we need: 8 B
For BC we need: 15 B
For BC we need: 21 C
For CA we need: 16 C
For CA we need: 4 A
For A we need: 45 ORE
For B we need: 64 ORE
For C we need: 56 ORE
"""
      if input_el != 'ORE':
        needed[input_el] += needed_input_count
        if input_el not in needed_elements:
          needed_elements.append(input_el)
      else:
        needed_ore += needed_input_count

  needed[needed_el] = 0

print(reactions)
print(needed)

print([el for el, c in needed.items() if c > 0])
print(needed_ore)
print(available)

# 31
# 5408
# 237639
# 237639
# 517381

# 867586 <- GOOD
