
class GameException(Exception):
   def __init__(self, *args, **kwargs):
      msg = self.init(*args, **kwargs)
      super().__init__(msg)

class AlreadyActivatedTree(GameException):
   def init(self, cell):
      return f'Tree on cell {cell} is dormant'

class CellNotEmptyException(GameException):
   def init(self, cell):
      return f'Already a tree on {cell}'

class CellNotFoundException(GameException):
   def init(self, cell):
      return f'Cell {cell} not found'

class CellNotValidException(GameException):
   def init(self, cell):
      return f'Cell {cell} not valid'

class NotEnoughSunException(GameException):
   def init(self, sun, cost):
      return f'Not enough sun to perform that action. Have {sun}, need {cost}.'

class NotOwnerOfTreeException(GameException):
   def init(self, cell):
      return f'You do not own the tree on cell {cell}'

class TreeAlreadyTallException(GameException):
   def init(self, cell):
      return f'Tree on cell {cell} is already max height'

class TreeIsSeedException(GameException):
   def init(self, cell):
      return f'Seed on cell {cell} cannot produce new seeds.'

class TreeNotFoundException(GameException):
   def init(self, cell):
      return f'There is no tree on cell {cell}'

class TreeNotTallException(GameException):
   def init(self, cell):
      return f'Tree on cell {cell} is not yet tall enough'

class TreeTooFarException(GameException):
   def init(self, start, end):
      return f'Too far to drop a seed (from cell {start} to cell {end})'
