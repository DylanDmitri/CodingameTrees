
class Cell:
   def __init__(self, index, richness):
      self.index = index
      self.richess = richness
      self.valid = True

class NullCell(Cell):
   def __init__(self):
      self.index = -1
      self.richness = 0
      self.valid = False

NO_CELL = NullCell()

