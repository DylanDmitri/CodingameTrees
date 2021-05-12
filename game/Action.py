

class Action:
   def __init__(self, source=None, target=None):
      self.source = source
      self.target = target
   
   def isGrow(self):
      return False
   
   def isComplete(self):
      return False
   
   def isSeed(self):
      return False
   
   def isWait(self):
      return False

class CompleteAction(Action):
   def isComplete(self):
      return True

class GrowAction(Action):
   def isGrow(self):
      return True

class SeedAction(Action):
   def isSeed(self):
      return True

class WaitAction(Action):
   def isWait(self):
      return True

class NoAction(Action):
   pass