from math import floor


def base_fuel_required(mass):
  return floor(mass / 3) - 2


modules = \
  [int(module) for module in open("input.txt").readlines()]


def fuel_required(mass):
  total_fuel = base_fuel_required(mass)
  additional_fuel = total_fuel
  while True:
    print("Fuel so far %s" % total_fuel)
    additional_fuel = base_fuel_required(additional_fuel)

    if additional_fuel <= 0:
      return total_fuel

    total_fuel += additional_fuel


total_fuel = sum([fuel_required(module) for module in modules])

print(total_fuel)

# 4941976
# 4944796
# 4944797
