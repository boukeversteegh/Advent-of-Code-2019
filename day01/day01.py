from math import floor


def base_fuel_required(mass):
  return floor(mass / 3) - 2


modules = \
  [int(module) for module in open("input.txt").readlines()]


def fuel_required(mass):
  base_fuel = base_fuel_required(mass)

  if base_fuel < 1:
    return 0

  extra_fuel = fuel_required(base_fuel)
  return base_fuel + extra_fuel


total_fuel = sum([fuel_required(module) for module in modules])

print(total_fuel)

# 4944796
# 4944797
# 4941976  <-- part 2 correct
