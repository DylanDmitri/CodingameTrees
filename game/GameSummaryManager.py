from game.Config import Config

class GameSummaryManager:

   def __init__(self):
      self.lines = []

   def addPlayerBadCommand(self, player, exception):
      self.lines.append(
         '{} provided invalid input. Exception "{}"'.format(
            'player', # player.nickname()
            exception
         ))

   def addPlayerTimeout(self, player):
      self.lines.append('player has not provided an action in time')

   def addPlayerDisqualified(self, player):
      self.lines.append('player was disqualified')

   def addCutTree(self, player, cell, score):
      self.lines.append('{} harvests tree on cell {}, scoring {} points'.format(
         'player', cell, score
      ))

   def addGrowTree(self, player, cell):
      self.lines.append(f'player in growing a tree on cell {cell}')

   def addPlantSeed(self, player, target, source):
      self.lines.append(
         f'player plants a seed on {target} from {source}')

   def addWait(self, player):
      self.lines.append(f'player is waiting')

   def addRound(self, round_num):
      self.lines.append(f'round {round_num}/{Config.MAX_ROUNDS}')
   
   def addError(self, error):
      self.lines.append(error)

   def addSeedConflict(self, location):
      self.lines.append(f'seed conflict at {location}')

   def __str__(self):
      return '\n'.join(self.lines)

   def addRoundTransition(self, round):
      self.lines.append(f"round {round} ends")

      if round+1 < Config.MAX_ROUNDS:
         direction = (round+1) % 6
         self.lines.append(f"The sun is now point towards direction {direction}")
         self.lines.append('-'*50)
         self.lines.append(f"round {round+1} begins")
    
   def addGather(self, player, gained):
      self.lines.append(f"player has collected {gained} sun points")