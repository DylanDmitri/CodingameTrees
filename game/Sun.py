
class Sun:
   def __init__(self):
      self.orientation = 0
   
   def move(self):
      self.orientation += 1
      self.orientation %= 6