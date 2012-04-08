'''
@author: Paulo Cheque (paulocheque@gmail.com)
'''

import threading, time, copy, yaml
from string import Template
from domain import dataobjects
from gameengine import utils, commands, errors, threading2
from gameengine.logger import logger

###############################################################################
# Context
    
class Context(utils.Observer):
  '''
  A context contains the content that a player can see to decide what to do.
  Summary of context return a string that contains a short description of the state of that context.
  All contexts has currentGamePlayers, and historicOfCommands
  
  Example of usage:
  
  class Context(game.Context):
    def __init__(self):
      super(Context, self).__init__()
      # some variables
      
    def notifyGameCommand(self, event):
      #need implementation
      pass
      
    def notifyPlayerCommand(self, event):
      #need implementation
      pass
  '''
  
  # Double dispatch, performance?
  # event.command.notify(self)
  
  def __init__(self):
    self.player = None
    self.currentGamePlayers = None
    self.configurations = None
    
  def __str__(self):
    return self.summary()
  
  def summary(self):
    '''
    Description of the context state 
    '''
    return yaml.dump(self, default_flow_style=False, explicit_start=True)
  
  def notify(self, event):
    self.currentGamePlayers = event.game.players # FIXME name only?
    self.configurations = event.game.configurations
    if isinstance(event.command, commands.GameCommand):
      self.notifyGameCommand(event)
    if isinstance(event.command, commands.PlayerCommand):
      self.notifyPlayerCommand(event)
  
  def notifyGameCommand(self, event): pass
  def notifyPlayerCommand(self, event): pass

###############################################################################

# Collecting Parameter
class GameReport(object):
  '''
  Report has report of all commands (good to debug and undertandings algorithms)
  
  Example of usage:
  
  from gameengine import game
  
  class GameReport(game.GameReport):
    def __init__(self):
      super(GameReport, self).__init__()
      # other variables
    
  #import copy
  #Important: Clone objects to avoid that bad strategies change the model without commands
  '''
  
  def __init__(self):
    self.game = None
    self.players = []
    self.initialNumberOfPlayers = 0
    self.configurations = None
    self.winners = []
    self.losers = []
    self.playersDurationTime = {}
    self.durationTime = 0
    self.commands = [] # [(command, [contexts after command])]
    self.exception = None
    
  def __str__(self):
    return self.summary()
  
  def simpleSummary(self):
    t = Template(
'''
- Message = ${message}
- durationTime = ${durationTime}
- ${initialNumberOfPlayers} player(s): ${players}
- winners: ${winners}
- losers: ${losers}
  
- commands: 
  ${commands}
  
- playersDurationTime: 
  ${playersDurationTime}
''')
    
    players = ', '.join(player for player in self.players)
    winners = ', '.join(winner.name for winner in self.winners)
    losers = ', '.join(loser.name for loser in self.losers)
    commands = '\n  '.join(command.summary() for command,contexts in self.commands)
    playersDurationTime = ''
    for player,times in self.playersDurationTime.items():
      formattedTimes = ', '.join(('%.3f' % time) for time in times)
      playersDurationTime += '\n  ' + player + ': ' + formattedTimes
    message = 'OK'
    if self.exception is not None: message = self.exception.message
    return t.substitute(
                 game=self.game,
                 players=players, 
                 initialNumberOfPlayers=self.initialNumberOfPlayers, 
                 configurations=self.configurations,
                 winners=winners,
                 losers=losers,
                 commands=commands,
                 durationTime=self.durationTime,
                 playersDurationTime=playersDurationTime,
                 message=message)
  
  def summary(self):
    t = Template(
'''
${game} Game Report:
${simpleSummary}
- configurations = ${configurations}
''')
    return t.substitute(
                 game=self.game,
                 simpleSummary=self.simpleSummary(),
                 configurations=self.configurations)
  
  def addPlayers(self, listOfPlayers):
    for player in listOfPlayers: self.players.append(player.name)
    
  def addWinners(self, *listOfWinners):
    for winner in listOfWinners: self.winners.append(winner)
    
  def addLosers(self, *listOfLosers):
    for loser in listOfLosers: self.losers.append(loser)
  
  def addCommand(self, command, contexts):
    self.commands.append((command, contexts[:])) # FIXME copy?
  
  def addPlaysDuration(self, player, durationTime):
    if player.name not in self.playersDurationTime:
      self.playersDurationTime[player.name] = []
    self.playersDurationTime[player.name].append(durationTime)
    
###############################################################################
    
class Configurations(object):
  def __init__(self, timeForCommand=-1, timeForPlay=-1, timeForGame=-1):
    '''
    # timeForCommand: default -1 = infinite
    # timeForPlay: default -1 = infinite  
    # timeForGame: default -1 = infinite
    
    # super(Configurations, self).__init__([, timeForCommand=-1][, timeForPlay=-1][, timeForGame=-1])
    class Configurations(game.Configurations):
      def __init__(self):
        super(Configurations, self).__init__(timeForCommand, timeForPlay, timeForGame)
      # other attributes here
    '''
    self.timeForCommand = timeForCommand
    self.timeForPlay = timeForPlay
    self.timeForGame = timeForGame
    
  def __str__(self):
    return self.summary()
  
  def summary(self):
    return yaml.dump(self, default_flow_style=False, explicit_start=True)
    
###############################################################################
    
class StartGameCommand(commands.GameCommand):
  '''
  # Some work before the game/round is started, like give cards to players, community cards, chips, etc
  '''
  
  def execute(self, game): pass

class EndGameCommand(commands.GameCommand):
  '''
  # Some work after the game/round is finished, like log something in report or count points...
  '''
  
  def execute(self, game): pass

class PlayerPlaysGameCommand(commands.GameCommand):
  '''
  # Some work before a player plays, like clean variables
  '''
  
  def execute(self, game): pass
    
###############################################################################
    
# Collecting Parameter: reportCollector
class AbstractGame(utils.Observable):
  '''
  Define a skeleton of a game.
  '''
  
  def __init__(self, players, 
               configurations=Configurations(), 
               commandsManager=commands.SynchronousCommandsManager(),
               reportCollector=GameReport(),
               startCommand=StartGameCommand(), 
               endCommand=EndGameCommand(), 
               playerplaysCommand=PlayerPlaysGameCommand()): 
    self.players = players
    self.configurations = configurations
    self.commandsManager = commandsManager
    self.commandsManager.game = self
    self.startCommand = startCommand
    self.endCommand = endCommand
    self.playerplaysCommand = playerplaysCommand
    
    self.commandsManager.registerCommand(self.startCommand.__class__)
    self.commandsManager.registerCommand(self.endCommand.__class__)
    self.commandsManager.registerCommand(self.playerplaysCommand.__class__)
    
    self.reportCollector = reportCollector
    self.reportCollector.addPlayers(self.players)
    self.reportCollector.configurations = self.configurations
    self.reportCollector.initialNumberOfPlayers = self.numberOfPlayers()
    self.reportCollector.game = self.__class__.name()
    
    super(AbstractGame, self).__init__()
    for player in self.players:
      self.registerObserver(player.context)
    self.permission = threading.RLock()
    self.thread = None
  
  def __str__(self):
    return self.name()
  
  @classmethod
  def name(clazz):
    return clazz.__name__.replace('Game', '')
  
  def start(self):
    logger.debug('\nStart game')
    startTime = time.clock()
    try:
      self.thread = threading2.KThread(target=self.run, name='Thread-Game')
      self.thread.daemon = True
      self.thread.start()
      self.thread.joinWithTimeout(self.configurations.timeForGame)
      if self.thread.isExpired():
        raise errors.TimeoutGameError()
    except Exception, e:
      logger.debug('Error in game: ' + e.message)
      self.reportCollector.exception = e
      raise e
    finally:
      endTime = time.clock()
      self.reportCollector.durationTime = (endTime - startTime)
      logger.debug('End game')
      logger.info('Winners: ' + ' '.join(winner.name for winner in self.winners()))
      
  def stop(self):
    logger.debug('Game stopped')
    self.thread.kill()
    
  # Template Method
  def run(self):
    logger.debug('Running...')
    self.commandsManager.start()
    self.commandsManager.addCommand(self.startCommand)
    self.play()
    self.reportCollector.winners = self.winners()
    self.commandsManager.addCommand(self.endCommand)
    self.commandsManager.stop()
    logger.debug('ok')
    
  def playerPlays(self, commandsManager, player):
    logger.debug('Player playing: ' + player.name)
    self.commandsManager.addCommand(self.playerplaysCommand)
    startTime = time.clock()
    thread = threading2.KThread(target=player.play, 
                                args=[commandsManager],
                                name='Thread-Player-' + player.name)
    try:
      thread.daemon = True
      thread.start()
      thread.joinWithTimeout(self.configurations.timeForPlay)
    finally:
      endTime = time.clock()
      self.reportCollector.addPlaysDuration(player, float(endTime - startTime))
      logger.debug('Total of %s-strategy iteration: %ss' % (player.name, str(endTime - startTime)))
      if thread.isExpired():
        raise errors.TimeoutStrategyError(player.name + ' - ' + str(endTime - startTime) + 's')
      logger.debug('Player stop playing: ' + player.name)
        
  def removePlayer(self, player):
    self.players.remove(player)
    self.reportCollector.addLosers(player)
    
  def numberOfPlayers(self):
    return len(self.players)
  
  def winners(self):
    winners = []
    for player in self.players:
      if self.conditionToWin(player):
        winners.append(player)
    return winners

  def report(self):
    return self.reportCollector
  
  def isTheEnd(self):
    '''
    Define a logic that return True or False to determine if the turn is over
    '''
    return len(self.winners()) > 0
  
  def play(self):
    raise NotImplementedError()
  
  def conditionToWin(self, player): 
    '''
    Define a logic that return True if a player win this turn, else returns False
    '''
    raise NotImplementedError()
  
  def notifyExecutedCommand(self, command):
    logger.debug('Notifing observers')
    self.reportCollector.addCommand(command, self.observers)
    self.notifyObservers(CommandEvent(self, command))

class Game(AbstractGame): pass

###############################################################################

class CommandEvent(object):
  
  def __init__(self, game, command):
    self.game = game
    self.command = command

class Utils(object): pass

###############################################################################

class OrderPlayersStrategy(object):
  
  def __init__(self, players):
    self.players = players
    
  def removePlayer(self, player):
    self.players.remove(player)
    
  def next(self): pass
    
class RandomOrderPlayersStrategy(OrderPlayersStrategy):
  
  def next(self): pass
  
class CycleOrderPlayersStrategy(OrderPlayersStrategy):
  
  def next(self): pass
  
  
