
from Game import Game
from Player import Player

import random


class Decider:
   pass

class ezPlayer(Decider):
   def decide(self, gamestate):
      possible = gamestate.getPossibleMoves(self.player)
      print(possible)
      return random.choice(possible)


class GameManager:

   def __init__(self):
      self.players = None
      self.live = False

   def holdCompetition(self, p1, p2, seed=None):
      deciders = [p1, p2]
      self.players = [Player('p1'), Player('p2')]
      deciders[0].player = self.players[0]
      deciders[1].player = self.players[1]

      gamestate = Game(self, seed)

      self.live = True
      while self.live:
         gamestate.performGameUpdate()
         for d, p in zip(deciders, self.players):
            choice = d.decide(gamestate)
            breakpoint()
            p.parse_action(choice)
      
      gamestate.onEnd()
      breakpoint()

   def endGame(self):
      self.live = False

g = GameManager()

g.holdCompetition(ezPlayer(), ezPlayer())
