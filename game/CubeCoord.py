class CubeCoord:
   directions = [
      (+1, -1,  0),
      (+1,  0, -1),
      ( 0, +1, -1),
      (-1, +1,  0),
      (-1,  0, +1),
      ( 0, -1, +1),
   ]

   def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z

   def __hash__(self):
      result = 1
      result = 31*result + self.x
      result = 31*result + self.y
      result = 31*result + self.z
      return result

   def __eq__(self, other):
      return (self.x==other.x) and (self.y==other.y) and (self.z==other.z)
   
   def __add__(self, other):
      return CubeCoord(self.x+other.x, self.y+other.y, self.z+other.z)
   
   def neighbor(self, orientation, distance=1):
      return CubeCoord(
         self.x + self.directions[orientation][0] * distance,
         self.y + self.directions[orientation][1] * distance,
         self.z + self.directions[orientation][2] * distance,
      )

   def distanceTo(self, dst):
      return (abs(self.x-dst.x) + abs(self.y-dst.y) + abs(self.z-dst.z)) / 2

   def __str__(self):
      return f'<{self.x}, {self.y}, {self.z}>'

   def __repr__(self):
      return f'<{self.x}, {self.y}, {self.z}>'

   def getOpposite(self):
      return CubeCoord(-self.x, -self.y, -self.z)
   
