from Config import Config
import Action as Action

class Player:
   def __init__(self, nickname):
      self.nickname = nickname
      self.action = Action.NoAction
      self.sun = Config.STARTING_SUN
      self.waiting = False
      self.score = 0
      self.bonusScore = 0

   def reset(self):
      self.message = None
      self.action = action.NoAction
   
   def set_action(self, action):
      # all python, we can just use the action object
      self.action = action
