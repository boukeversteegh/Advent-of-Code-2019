import unittest


class Day8:

  def get_layers(self, values, width, height):
    layers = []
    size = width * height

    layer_index = 0
    while True:
      done = False
      layer = []

      layer_start = layer_index * size
      for y in range(0, height):
        row_start = layer_start + y * width

        # [0, 1, 2]
        if row_start > len(values) - 1:
          done = True
        else:
          layer.append(values[row_start:row_start + width])

      print(layer)

      if done:
        break

      layer_index += 1
      layers.append(layer)

    return layers

  def count_number(self, layer, number):
    count = 0
    for row in layer:
      for value in row:
        if value == number:
          count += 1

    return count

  def build_image(self, layers, width, height):
    image = []

    for y in range(0, height):
      image.append([])
      for x in range(0, width):
        for layer in layers:
          val = layer[y][x]
          if val != 2:
            image[y].append(val)
            break

    return image



class ExamplesDay8(unittest.TestCase):

  def test_part1(self):
    pass


class SolutionsDay8(unittest.TestCase):

  def __init__(self, methodName: str = ...) -> None:
    super().__init__(methodName)
    self.d = Day8()
    with open('day08/input.txt') as f:
      self.values = [int(val) for val in f.readlines()[0].strip()]

  def test_part1(self):
    layers = self.d.get_layers(self.values, 25, 6)

    layer0 = min(layers, key=lambda layer: self.d.count_number(layer, 0))

    n1s = self.d.count_number(layer0, 1)
    n2s = self.d.count_number(layer0, 2)

    print(n1s * n2s)



  def test_part2(self):
    d = self.d
    width = 25
    height = 6
    layers = d.get_layers(self.values, width, height)
    image = d.build_image(layers, width, height)

    for y in range(0, height):
      for x in range(0, width):
        val = image[y][x]
        if val == 0:
          print('#', end="")
        else:
          print(' ', end="")

      print("")
    # GZKJY
