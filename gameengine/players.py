'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import re, time, copy
from domain import dataobjects
from gameengine import utils, game, errors

###############################################################################
# Player
  
class Player(dataobjects.ValueObject):
  '''
  from gameengine import game
  game.Player('name', StrategyClass, game.Team('name'))
  '''
  
  def __init__(self, name, strategy, team=None, contextClass=game.Context):
    self.name = name
    self.strategy = strategy
    self.team = team
    if team == None:
      self.team = Team(name)
      self.team.addPlayer(self)
    self.context = contextClass()
    # links
    self.context.player = self
    self.strategy.player = self
    self.strategy.context = self.context
  
  def __str__(self):
    return self.name
  
  def equalsVariables(self):
    return ['name']

  # Template method for strategy pattern
  def play(self, commandsManager):
    self.strategy.play(commandsManager)
  
Player.addConstraints('name', Nullable = False, Min = 1, Max = 15)
Player.addConstraints('strategy', Nullable = False)

###############################################################################
# Team

class Team(dataobjects.ValueObject):
  '''
  from gameengine import game
  game.Team(...)
  '''
  
  def __init__(self, name):
    self.name = name
    self.players = []
    
  def equalsVariables(self):
    return ['name']
    
  def addPlayer(self, player):
    self.players.append(player)
    
  def numberOfPlayers(self):
    return len(self.players)
    
Team.addConstraints('name', Nullable = False, Min = 1, Max = 15)
Team.addConstraints('strategy', Nullable = False)


###############################################################################
# Strategy

class Strategy(object):
  '''
  Example of usage:
  
  from gameengine import game
  
  class MyStrategy(players.Strategy):
  
    def play(self, commandsManager):
      self.stepone(commandsManager)
      self.steptwo(commandsManager)
        
    def stepone(self, commandsManager):
      # implementation here, example:
      if self.context.something == anotherthing:
        mycommand = MyCommand(self.player, self.params)
        if mycommand.isValid(self.context):
          commandsManager.addCommand(mycommand)
      
    def steptwo(self, commandsManager):
      # implementation here, example:
      pass
      
  # now you can instantiate your player with it: game.Player('MyPlayer', MyStrategy())
  '''
  
  def __init__(self):
    self.player = None
    self.context = None
    
  def play(self, commandsManager):
    raise NotImplementedError()
  
###############################################################################

class SafeStrategy(Strategy):
  '''
  To create easy extension of algorithms
  '''
  
  builtinFunctions = [
    'str', 'bool', 'int', 'float', 'complex', 'divmod',
    'dict', 'list', 'tuple', 'set', 'hex', 'oct', 
    'min', 'max', 'any', 'all', 'map', 'sum', 'abs', 'len', 'filter', 'range',
    'zip', 'slice', 'reversed', 'sorted',  'enumerate',
    'hash', 'frozenset', 'iter',
    'repr', 'ord', 'pow', 'chr']
    #'print', 'id', 
    # 2.5 problem: 'bin', 'format', 'bytes', 'next'
  
  def __init__(self, accessibleClasses=[]):
    self.accessibleClasses = accessibleClasses
  
  def getPythonEnvironment(self):
    builtins = {}
    builtinsMap = globals()['__builtins__']
    for builtinFunction in self.builtinFunctions:
        builtins[builtinFunction] = builtinsMap[builtinFunction]
    globalsenv = {'__builtins__': builtins} # FIXME estudar
    globalsenv['True'] = True
    globalsenv['False'] = False
    globalsenv['re'] = globals()['re']
    return globalsenv
  
  def getGameEnvironment(self, commandsManager):
    localsMap = {'context': self.context, 'player': self.player, 'addCommand': commandsManager.addCommand}
    for command in commandsManager.validCommands:
      localsMap[command.__name__] = command
    for clazz in self.accessibleClasses:
      localsMap[clazz.__name__] = clazz
    return localsMap
  
  def getGlobalEnvironment(self, commandsManager):
    globalEnvironment = {}
    globalEnvironment.update(self.getPythonEnvironment())
    globalEnvironment.update(self.getGameEnvironment(commandsManager))
    return globalEnvironment
  
  def play(self, commandsManager):
    pass
    
  def validate(self):
    if self.sourceContainsString('import '):
      raise errors.MailiciousStrategyError()
    forbiddenFunctions = ['eval\(', 'exec\(', 'compile\(', 'open\(']
    for forbiddenFunction in forbiddenFunctions:
      if self.sourceContainsString(forbiddenFunction):
        raise errors.MailiciousStrategyError()
    if self.sourceContainsString('.game'):
      raise errors.CheatStrategyError()
    
  def sourceContainsString(self, string):
    return re.search(string, self.sourcecode) != None

###############################################################################

class InteractiveStrategy(SafeStrategy):
  
  def interactiveCommand(self, commandsManager):
    command = raw_input('\n>>> ')
    if command.strip() == '': return False
    eval(command, self.getGlobalEnvironment(commandsManager), {})
    return True
  
  def play(self, commandsManager):
    while True:
      if not self.interactiveCommand(commandsManager):
        break
  
###############################################################################
  
class RuntimeStrategy(SafeStrategy):
  '''
  To create easy extension of algorithms
  '''
  
  def __init__(self, sourcecode, accessibleClasses=[]):
    super(RuntimeStrategy, self).__init__(accessibleClasses)
    self.sourcecode = sourcecode
  
  def play(self, commandsManager):
    exec(self.sourcecode, self.getGlobalEnvironment(commandsManager), {})
    
  def validate(self):
    if self.sourceContainsString('import '):
      raise errors.MailiciousStrategyError()
    forbiddenFunctions = ['eval\(', 'exec\(', 'compile\(', 'open\(']
    for forbiddenFunction in forbiddenFunctions:
      if self.sourceContainsString(forbiddenFunction):
        raise errors.MailiciousStrategyError()
    if self.sourceContainsString('.game'):
      raise errors.CheatStrategyError()
    
  def sourceContainsString(self, string):
    return re.search(string, self.sourcecode) != None
