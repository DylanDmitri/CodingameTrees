from game.Cell import Cell
from game.Constants import Constants
from game.Config import Config
from game.CubeCoord import CubeCoord

import random

class Board:

   def __init__(self, seed):
      self.tiles = {}  # coord -> Cell
      self.index = 0

      if seed:
         random.seed(seed)
      self.generate()

   def generateCell(self, coord, richness):
      self.tiles[coord] = Cell(self.index, richness)
      self.index += 1

   def generate(self):

      # build forest floor
      center = CubeCoord(0, 0, 0)
      self.generateCell(center, Constants.RICHNESS_LUSH)

      coord = center.neighbor(0)

      for distance in range(1, Config.MAP_RING_COUNT+1):
         for orientation in range(6):
            for _ in range(distance):
               if distance == Config.MAP_RING_COUNT:
                  self.generateCell(coord, Constants.RICHNESS_POOR)
               elif distance == Config.MAP_RING_COUNT -1:
                  self.generateCell(coord, Constants.RICHNESS_OK)
               else:
                  self.generateCell(coord, Constants.RICHNESS_LUSH)
               coord = coord.neighbor((orientation + 2) % 6)
         coord = coord.neighbor(0)

      # add random holes
      coordList = list(self.board.keys())
      wantedEmptyCells = random.randint(1, Config.MAX_EMPTY_CELLS) if Config.HOLES_ENABLED else 0
      actualEmptyCells = 0

      while actualEmptyCells < wantedEmptyCells-1:
         randCord = random.choice(coordList)

         if self.board[randCord].richness == Constants.RICHNESS_NULL:
            continue

         self.board[randCord].richness = Constants.RICHNESS_NULL
         self.board[randCord.getOpposite()].richness = Constants.RICHNESS_NULL
         actualEmptyCells += 1 if randCord is center else 2


"""
coordinates = list(self.board.keys)
wantedEmpty = 5

while (count with null richness) < wantedEmptyCells

   set richness to 0 for [
      a random coordinate with some richness,
      it's opposite
   ]




"""