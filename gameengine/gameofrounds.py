'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import time, copy, threading 
from string import Template
from domain import dataobjects
from gameengine import game, players, utils, commands, errors, threading2

###############################################################################

class Context(game.Context):
  '''
  class Context(gameofrounds.Context):
    def __init__(self):
      super(Context, self).__init__()
      # other attributes here
      
    def notifyGameOfRoundsCommand(self, event):
      #need implementation
      pass
      
    def notifyRoundCommand(self, event):
      #need implementation
      pass
      
    def notifyPlayerCommand(self, event):
      #need implementation
      pass
  '''
  
  def __init__(self):
    super(Context, self).__init__()
    self.numberOfRounds = 0
  
  def notify(self, event):
    super(Context, self).notify(event)
  
  def notifyGameCommand(self, event):
    if isinstance(event.game, GameOfRounds):
      self.numberOfRounds = event.game.numberOfRounds()
      self.notifyGameOfRoundsCommand(event)
    else:
      self.notifyRoundCommand(event)
      
  def notifyGameOfRoundsCommand(self, event): pass
  def notifyRoundCommand(self, event): pass
  def notifyPlayerCommand(self, event): pass

###############################################################################

class GameOfRoundsConfigurations(game.Configurations):
  '''
  # timeForCommand: default -1 = infinite
  # timeForPlay: default -1 = infinite  
  # timeForGame: default -1 = infinite
  # super(Configurations, self).__init__([, timeForCommand=-1][, timeForPlay=-1][, timeForGame=-1][, numberOfRounds=-1])
  class GameOfRoundsConfigurations(gameofrounds.GameOfRoundsConfigurations):
    def __init__(self):
      super(GameOfRoundsConfigurations, self).__init__(timeForCommand, timeForPlay, timeForGame, numberOfRounds)
      # other attributes here
  '''
  
  def __init__(self, timeForCommand=-1, timeForPlay=-1, timeForGame=-1, numberOfRounds=-1):
    super(GameOfRoundsConfigurations, self).__init__(timeForCommand, timeForPlay, timeForGame)
    self.numberOfRounds = numberOfRounds
    
###############################################################################

# Collecting Parameter
class RoundReport(game.GameReport):
  
  def summary(self):
    t = Template(
'''
Round Report:
${simpleSummary}
''')
    return t.substitute(simpleSummary=self.simpleSummary())
    
# Collecting Parameter
class GameOfRoundsReport(game.GameReport):
  '''
  roundsReports
  '''
  
  def __init__(self):
    super(GameOfRoundsReport, self).__init__()
    self.roundsReports = []
    
  def addRoundReport(self, roundReport):
    self.roundsReports.append(roundReport)
    
  def summary(self):
    t = Template(
'''
${gameReport}
${numberOfRounds} Rounds Reports:
${roundsReports}
''')
    gameReport = super(GameOfRoundsReport, self).summary()
    roundsReports = '\n  '.join(round.summary() for round in self.roundsReports)
    return t.substitute(numberOfRounds=len(self.roundsReports), gameReport=gameReport, roundsReports=roundsReports)
    


class StartGameRoundCommand(commands.GameCommand):
  def execute(self, round): pass

class EndGameRoundCommand(commands.GameCommand):
  def execute(self, round): pass


class GameRound(game.AbstractGame):
  
  def __init__(self, game, players, 
               configurations=game.Configurations(), 
               commandsManager=commands.SynchronousCommandsManager(),
               reportCollector=game.GameReport(),
               startCommand=StartGameRoundCommand(), 
               endCommand=EndGameRoundCommand(), 
               playerplaysCommand=game.PlayerPlaysGameCommand()): 
    super(GameRound, self).__init__(players, configurations, commandsManager,
                               reportCollector, startCommand, endCommand, playerplaysCommand)
    self.game = game
    
  def play(self): pass
  def conditionToWin(self, player): raise NotImplementedError()

###############################################################################

# Observer pattern: Observable
class GameOfRounds(game.Game):
  
  def __init__(self, players, 
               configurations=GameOfRoundsConfigurations(), 
               commandsManager=commands.SynchronousCommandsManager(),
               reportCollector=GameOfRoundsReport(),
               startCommand=game.StartGameCommand(), 
               endCommand=game.EndGameCommand(), 
               playerplaysCommand=game.PlayerPlaysGameCommand(),
               roundClass=GameRound): 
    super(GameOfRounds, self).__init__(players, configurations, commandsManager,
                               reportCollector, startCommand, endCommand, playerplaysCommand)
    self.roundClass = roundClass
    self.rounds = []
    self.currentRound = None
  
  def newRound(self):
    # FIXME strategy of who starts
    # Prototype style with reflection: roundClass
    if self.configurations.numberOfRounds < 0 or self.numberOfRounds() < self.configurations.numberOfRounds:
      self.currentRound = self.roundClass(self, self.players[:], self.configurations, self.commandsManager)
    
  def numberOfRounds(self):
    return len(self.rounds)
  
  def play(self):
    while len(self.players) > 0 and not self.isTheEnd():
      self.newRound()
      self.currentRound.start()
      self.rounds.append(self.currentRound)
      self.reportCollector.addRoundReport(self.currentRound.report())


