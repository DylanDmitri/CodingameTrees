
from CubeCoord import CubeCoord
from Config import Config
from Cell import Cell, NO_CELL
from Constants import Constants
from Board import Board
from Tree import Tree
from Action import *

import random

GATHER_FRAME = 0
ACTION_FRAME = 1
SUN_MOVE_FRAME = 2

class Game:

   #  @Inject private MultiplayerGameManager<Player> gameManager;
   #  @Inject private GameSummaryManager gameSummaryManager;

   INIT_NUTRIENTS = Config.STARTING_NUTRIENTS
   SEED_ENABLED = True
   GROW_ENABLED = True
   SHADOW_ENABLED = True
   HOLES_ENABLED = True

   MAX_ROUNDS = 24
   STARTING_TREE_COUNT = Constants.STARTING_TREE_COUNT
   STARTING_TREE_SIZE = Constants.TREE_SMALL
   STARTING_TREE_DISTANCE = 2
   STARTING_TREES_ON_EDGES = True

   def __init__(self, gameManager, seed=None):
      self.gameManager = gameManager

      self.board = Board(seed)  # Board 
      self.trees = {}    # index -> Tree
      self.dyingTrees = []  # list<CubeCoord>
      self.availibleSun = []
      self.sentSeeds = []
      self.initStartingTrees(seed)
      self.nutrients = self.INIT_NUTRIENTS

      self.sun = None    # Sun
      self.shadows = {}  # int -> int
      self.cells = []
      self.frameType = GATHER_FRAME

      self.round = 0
      self.turn = 0
   
   def getExpected():
      return 'SEED', 'GROW', 'COMPLETE', 'WAIT'

   def getCoordByIndex(self, idx):
      # todo cashe the keys
      return tuple(self.board.map.keys())[idx]
   
   def initStartingTrees(self, seed):
      center = CubeCoord(0, 0, 0)

      coords = self.board.map
      if self.STARTING_TREES_ON_EDGES:
         startingCoords = [c for c in coords if c.distanceTo(center) == Config.MAP_RING_COUNT]
      else:
         startingCoords = [c for c in coords if c != center]
      
      startingCoords = [c for c in startingCoords if self.board.map[c].richness != Constants.RICHNESS_NULL]

      validCoords = []
      while len(validCoords) < self.STARTING_TREE_COUNT*2:
         validCoords = self.tryInitStartingTrees(startingCoords, seed)
      iterValidCoord = iter(validCoords)
      
      players = self.gameManager.players
      for i in range(self.STARTING_TREE_COUNT):
         self.placeTree(players[0], self.board.map.get(next(iterValidCoord)).index, self.STARTING_TREE_SIZE)
         self.placeTree(players[1], self.board.map.get(next(iterValidCoord)).index, self.STARTING_TREE_SIZE)
   
   def tryInitStartingTrees(self, startingCoords, seed):
      if not startingCoords:
         return []
      if seed:
         random.seed(seed+999)

      coordinates = []
      availableCoords = startingCoords[:]

      for i in range(self.STARTING_TREE_COUNT):

         normalCoord = random.choice(availableCoords)
         otherCoord = normalCoord.getOpposite()

         availableCoords = [c for c in availableCoords if 
            (c.distanceTo(normalCoord) >= self.STARTING_TREE_DISTANCE) and
            (c.distanceTo(otherCoord)  >= self.STARTING_TREE_DISTANCE)]

         coordinates.append(normalCoord)
         coordinates.append(otherCoord)
      
      return coordinates

   def calculateShadows(self):
      """
      clear Shadows
      
      each tree
         each neighbor (1..size) steps in (sun direction)
            increment Shadow value by tree size
      """
      self.shadows = {}

      for idx, tree in enumerate(self.trees):
         coord = self.board.map.get(idx)

         for i in range(tree.size):
            tempCoord = coord.neighbor(sun.getOrientation(), i)
            if tempCoord in board.map:
               oldValue = shadows.get(tempCoord, 0)
               shadows[tempCoord] = max(oldValue, tree.size)
   
   def getCoordsInRange(self, center, N):
      results = []
      for x in range(-N, N):
         for y in range(max(-N, -x-N), min(N, -x+N)+1):
            z = -x - y 
            results.append(center + CubeCoord(x, y, z))
      return results
   
   def getPossibleMoves(self, player):
      lines = ['WAIT']

      if player.waiting:
         return lines
      
      # for each tree, where they can seed & if they can grow

      seedCost = self.getSeedCost(player)

      for idx, tree in self.trees.items():
         if tree.owner != player:
            continue

         location = self.getCoordByIndex(idx)

         if self.playerCanSeedFrom(player, tree, seedCost):
            for targetCoord in self.getCoordsInRange(location, tree.size):
               targetCell = self.board.map.get(targetCoord, NO_CELL)
               print(targetCoord, targetCell.index)
               if self.playerCanSeedTo(targetCell, player):
                  lines.append(f'SEED {idx} {targetCell.index}')

         print(lines)
         breakpoint()

         growCost = self.getGrowthCost(tree)
         if growCost <= player.sun and (not tree.isDormant):
            if tree.size == Constants.TREE_TALL:
               lines.append(f'COMPLETE {index}')
            elif self.GROW_ENABLED:
               lines.append(f'GROW {index}')

      return lines

   def playerCanSeedFrom(self, player, tree, seedCost):
      return (self.SEED_ENABLED and
         seedCost <= player.sun and
         tree.size > Constants.TREE_SEED and
         not tree.isDormant)

   def playerCanSeedTo(self, targetCell, player):
      return (targetCell.valid and
         targetCell.richness != Constants.RICHNESS_NULL and
         targetCell.index not in self.trees)

   def getGrowthCost(self, tree):
      targetSize = tree.size + 1
      if targetSize > Constants.TREE_TALL:
         return Constants.LIFECYCLE_END_COST
      return self.getCostFor(targetSize, tree.owner)

   def getSeedCost(self, player):
      return self.getCostFor(0, player)

   def getCostFor(self, size, owner):
      return (
         Constants.TREE_BASE_COST[size]  # base cost
         + sum(t.size==size and t.owner==owner for t in self.trees.values())  # plus count of same trees
      )

   def doGrow(self, player, action):
      coord = self.getCoordByIndex(action.targetId)
      cell = board.map.get(coord)

      targetTree = trees.get(cell.getIndex())
      if not targetTree:
         raise Exception('tree not found')
      if targetTree.owner != player:
         raise Exception('not owner of tree')
      if targetTree.isDormant:
         raise Exception('tree is sleepy')
      if tree.size >= Constants.TREE_TALL:
         raise Exception('tree already tall')

      growCost = self.getGrowthCost(targetTree)

      if player.sun < growCost:
         raise Exception('not enough sun')

      player.sun -= growCost
      targetTree.grow()
      gameSummaryManager.addGrowTree(player, cell)
      targetTree.dormant = True
   
   def doComplete(self, player, action):
      coord = self.getCoordByIndex(action.targetId)
      cell = board.map.get(coord)

      targetTree = trees.get(cell.index)
      if not targetTree:
         raise Exception('tree not found')
      if targetTree.owner != player:
         raise Exception('not your DAMN tree')
      if targetTree.size < Constants.TREE_TALL:
         raise Exception('too small for fall')
      if targetTree.dormant:
         raise Exception('your tree asleep')

      costOfGrowth = self.getGrowthCost(targetTree)
      if player.sun < costOfGrowth:
         raise Exception('not enough sun')
      player.sun -= costOfGrowth

      dyingTrees.append(coord)
      targetTree.dormant = True

   def doSeed(self, player, action):
      targetCoord = self.getCoordByIndex(action.targetId)
      sourceCoord = self.getCoordByIndex(action.sourceId)

      if cell.hasTree:
         raise Exception('yallready have a tree there')

      sourceTree = trees.get(sourceCell.index)
      if not sourceTree:
         raise Exception('no source tree found')

      if sourceTree.size == Constants.TREE_SEED:
         raise Exception('seed too small to make more seed')
   
      if tree.owner != player:
         raise Exception('not your tree')

      if tree.dormant:
         raise Exception('tree sleepy')

      distance = sourceCoord.distanceTo(targetCoord)
      if distance > sourceTree.getSize():
         raise Exception('too far to seed')
      if not targetCell.richness:
         raise Exception('invalid seed target')

      seedCost = self.getSeedCost(player)
      if player.sun < seedCost: 
         raise Exception('not enough sun')

      player.sun -= seedCost
      sourceTree.dormant = True

      self.sentSeeds.append(Seed(player.getIndex(), sourceCell, targetCell))
   
   def giveSun(self):
      toPlayers = [0, 0]
      for idx, tree in self.trees.items():
         if self.shadows.get(idx, 0) > tree.size:
            continue

         tree.owner.sun += tree.size
   
   def removeDyingTrees(self):
      for t in self.dyingTrees:
         cell = self.board.map.get(coord)

         points = self.nutrients
         if cell.richness == Constants.RICHNESS_OK:
            points += Constants.RICHNESS_BONUS_OK
         elif cell.richness == Constants.RICHNESS_LUSH:
            points += Constants.RICHNESS_BONUS_LUSH

         player = trees.get(cell.index).owner
         player.score += points
         trees.remove(cell.index)

   def updateNutrients(self):
      self.nutrients -= len(self.dyingTrees)

   def performGameUpdate(self):
      self.turn += 1

      {
         GATHER_FRAME: self.performSunGatheringUpdate,
         ACTION_FRAME: self.performActionUpdate,
         SUN_MOVE_FRAME: self.performSunMoveUpdate,
      }.get(self.frameType)()

      if self.round == Config.MAX_ROUNDS:
         self.gameManager.endGame()

   def performSunMoveUpdate(self):
      self.round += 1
      if self.round < self.MAX_ROUNDS:
         sun.move()
         self.calculateShadows()
      
      self.frameType = GATHER_FRAME

   def performSunGatheringUpdate(self):
      for p in self.gameManager.players:
         p.waiting = False

      for t in self.trees.values():
         t.reset()

      self.giveSun()
      self.frameType = ACTION_FRAME

   def performActionUpdate(self):
      for p in self.gameManager.players:
         if p.waiting:
            continue

         if p.action.isGrow():
            self.doGrow(p, action)
         elif p.action.isSeed():
            self.doSeed(p, action)
         elif p.action.isComplete():
            self.doComplete(p, action)
         else:
            p.waiting = True
         
      if self.seedsAreConflicting():
         gameSummaryManager.addSeedConflict(sentSeeds[0])
      else:
         for seed in self.sentSeeds:
            self.plantSeed(seed.owner, seed.target, seed.souce)

      self.removeDyingTrees()
      self.updateNutrients()

      if self.allPlayersAreWaiting():
         self.frameType = SUN_MOVE_FRAME

   def seedsAreConflicting(self):
      return len(self.sentSeeds)==2 and len(set(self.sentSeeds))==1

   def allPlayersAreWaiting(self):
      return all(p.waiting for p in self.gameManager.players)

   def plantSeed(self, player, index, parent):
      seed = self.placeTree(player, index, size=Constants.TREE_SEED)
      seed.dormant = True
      seed.parent = parent

   def placeTree(self, player, index, size):
      t = Tree(owner=player, size=size)
      self.trees[index] = t
      return t

   def onEnd(self):
      # increment each player's score by one-third of their sun
      p1, p2 = self.gameManager.players
      for player in (p1, p2):
         player.score += int(p.sun//3)
      
      p1.bonus_score += sum(t.owner==p1 for t in self.trees)
      p2.bonus_score += sum(t.owner==p2 for t in self.trees)
