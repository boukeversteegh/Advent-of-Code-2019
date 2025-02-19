import collections


class Intersector:
  def __init__(self) -> None:
    super().__init__()

    self.grid = collections.defaultdict(lambda: collections.defaultdict(lambda: {}))

  def trace_wires(self, lines):
    for wire_index, line in enumerate(lines):
      sections = line.split(',')

      self.trace_wire(sections, wire_index)

  def trace_wire(self, sections, wire_index):
    x, y = (0, 0)
    line_steps_total = 0
    for section in sections:
      section_direction = section[0]
      section_dist = int(section[1:])

      directions = {
        'U': (0, -1),
        'D': (0, 1),
        'L': (-1, 0),
        'R': (1, 0),
      }
      section_dx, section_dy = directions[section_direction]

      for i in range(0, section_dist):
        x += section_dx
        y += section_dy
        line_steps_total += 1

        if wire_index not in self.grid[y][x].keys():
          self.grid[y][x][wire_index] = line_steps_total

  def part1(self):
    min_x = 0
    min_y = 0
    min_distance = None

    for y, row in self.grid.items():
      for x, lines in row.items():
        if len(lines.items()) > 1:
          distance = abs(x) + abs(y)
          if min_distance is None or (distance < min_distance):
            print("Intersection at %s" % (((x, y), distance),))
            min_x = x
            min_y = y
            min_distance = distance

    print(((min_x, min_y), min_distance))

  def part2(self):
    min_x = 0
    min_y = 0
    min_time = None
    for y, row in self.grid.items():
      for x, line_times in row.items():
        if len(line_times.items()) > 1:
          time = sum(line_times.values())
          if min_time is None or (time < min_time):
            min_time = time
            min_x = x
            min_y = y
    print(((min_x, min_y), min_time))


def main():
  raw = open('input.txt').readlines()

  # raw = ['R8,U5,L5,D3', 'U7,R6,D4,L4']
  # raw = ['R75,D30,R83,U83,L12,D49,R71,U7,L72',
  #        'U62,R66,U55,R34,D71,R55,D58,R83']

  lines = [line.strip() for line in raw]
  intersector = Intersector()
  intersector.trace_wires(lines)
  intersector.part1()
  intersector.part2()


if __name__ == '__main__':
  main()

# 2923 WRONG
# 399  RIGHT

# 15678 PART TWO CORRECT
