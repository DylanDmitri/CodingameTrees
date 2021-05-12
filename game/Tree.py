
class Tree:
   def __init__(self, owner, size=0):
      self.size = size
      self.owner = owner
      self.parent = None  # set this later, Java Style
      self.isDormant = False
   
   def reset(self):
      self.isDormant = False

   def __str__(self):
      return f"{self.owner.nickname}'s {['seed', 'smol', 'med', 'tall'][self.size]} tree"
