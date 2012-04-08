'''

@author: Paulo Cheque (paulocheque@gmail.com)

Example of usage:

from gameengine import testhelper

class MyTestCaseClass(testhelper.GameEngineTests):
  pass

'''

import time

import unittest

from gameengine import game, gameofrounds, commands, players, utils, factory, errors

###############################################################################

class MyAssyncGame(game.Game):
  '''some documentation'''
  
  def __init__(self, players, configurations=game.Configurations()):
    super(MyAssyncGame, self).__init__(players, configurations, MyGameReport(), commands.AsynchronousCommandsManager())
    self.finish = False 
  
  def conditionToWin(self, player): return self.finish


class MyGame(game.Game):
  '''some documentation'''
  
  def __init__(self, players, configurations=game.Configurations()):
    commandsManager = commands.SynchronousCommandsManager()
    commandsManager.registerCommand(FinishCommand)
    commandsManager.registerCommand(NeutralCommand)
    commandsManager.registerCommand(InvalidCommand)
    commandsManager.registerCommand(BuggedCommand)
    commandsManager.registerCommand(SlowCommand)
    commandsManager.registerCommand(ParamsCommand)
    super(MyGame, self).__init__(players, configurations, commandsManager, MyGameReport())
    self.finish = False
    
  def conditionToWin(self, player): return self.finish
  
  def play(self):
    if self.configurations.timeForPlay == 6:
      print('playing')
    while(not self.isTheEnd()):
      for player in self.players:
        self.playerPlays(self.commandsManager, player)

###############################################################################

class FinishCommand(commands.PlayerCommand):
  def executeWithValidation(self, game): game.finish = True
  
class NeutralCommand(commands.PlayerCommand):
  def executeWithValidation(self, game): print('Hi!')
  
class UnknownCommand(commands.PlayerCommand):
  def executeWithValidation(self, game): return True
  
class InvalidCommand(commands.PlayerCommand):
  def validate(self, context):
    raise errors.InvalidCommandError(self) 
    return False
  def executeWithValidation(self, game): return True
  
class BuggedCommand(commands.PlayerCommand):
  def executeWithValidation(self, game): raise Exception('ops')
  
class SlowCommand(commands.PlayerCommand):
  def executeWithValidation(self, game):
    if self.params is None: duration = 0.5
    else: duration = self.params
    time.sleep(duration)
  
class ParamsCommand(commands.PlayerCommand):
  def executeWithValidation(self, game): print(self.params)

###############################################################################

class MyPlayerContext(game.Context):
  def __init__(self):
    super(MyPlayerContext, self).__init__()

###############################################################################

class MyStrategy(players.Strategy):
  
  def play(self, commandsManager):
    self.actionOne(commandsManager)
    self.actionTwo(commandsManager)
    
  def actionOne(self, commandsManager): pass
  def actionTwo(self, commandsManager): pass
  
class CycleStrategy(players.Strategy):
  
  def __init__(self):
    self.flag = 0
    
  def play(self, commandsManager):
    if self.flag == 0: 
      self.flag = 1
      commandsManager.addCommand(NeutralCommand(self.player, self.flag))
    if self.flag == 1: 
      self.flag = 0
      commandsManager.addCommand(NeutralCommand(self.player, self.flag))
  
###############################################################################
  
class MyGameReport(game.GameReport):
  
  def __init__(self):
    super(MyGameReport, self).__init__()
    self.mydata = 0
    
class MyGameOfRoundsReport(gameofrounds.GameOfRoundsReport):
  
  def __init__(self):
    super(MyGameOfRoundsReport, self).__init__()
    self.mydata = 0
  
###############################################################################

class MyConfigurations(game.Configurations):
  def __init__(self):
    super(MyConfigurations, self).__init__(3, 2, 3)
    
###############################################################################

class MyGameFactory(factory.GameFactory):
  
  def __init__(self):
    super(MyGameFactory, self).__init__(MyGame, MyPlayerContext, MyConfigurations)
    
###############################################################################
# Base Test Class:

class GameEngineTests(unittest.TestCase):

  def setUp(self):
    self.oneplayer = [players.Player('Player1', MyStrategy)]
    self.twoplayers = [players.Player('Player1', MyStrategy), players.Player('Player2', MyStrategy)]
    self.twoplayersWithSameTeam = [
                              players.Player('Player1', MyStrategy, team=players.Team('MyTeam')), 
                              players.Player('Player2', MyStrategy, team=players.Team('MyTeam'))]
    
    self.player = self.twoplayers[0]
    
    self.context = MyPlayerContext()
    
    self.params = None
    
    self.neutralcommand = NeutralCommand(self.player, self.params)
    self.unknowncommand = UnknownCommand(self.player, self.params)
    self.invalidcommand = InvalidCommand(self.player, self.params)
    self.buggedcommand = BuggedCommand(self.player, self.params)
    self.slowcommand = SlowCommand(self.player, self.params)
    self.paramscommand = ParamsCommand(self.player, 'myparam')
    
    self.strategy = MyStrategy
    
    self.gamereport = MyGameReport()
    self.gameofroundsreport = MyGameOfRoundsReport()
    
    self.configurations = MyConfigurations()
    
    self.game = MyGame(self.twoplayers, self.configurations)
    
    self.gamefactory = MyGameFactory()
    
    