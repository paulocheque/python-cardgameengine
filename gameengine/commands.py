'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import time
import threading
from string import Template
from domain import dataobjects
from gameengine import utils, errors, threading2
from gameengine.logger import logger

# Command
class GameCommand(object):
  '''
  Example of usage:
  
  from gameengine import game
  
  class StartGameCommand(commands.GameCommand):

    def execute(self, game):
      # some implementation here, example:
      game.removePlayer(self.player)
  '''
  
  def __init__(self):
    self.durationTime = 0
    
  @classmethod
  def name(clazz):
    return clazz.__name__.replace('Command', '')
  
  def __str__(self):
    return self.summary()
  
  def summary(self):
    t = Template('${command} - ${durationTime}s')
    return t.substitute(
                 command=self.name(), 
                 durationTime=self.durationTime)

  def execute(self, game):
    raise NotImplementedError()
  
  def process(self, game):
    startTime = time.clock()
    thread = None
    try:
      thread = threading2.KThread(target=self.execute, 
                                  args=[game],
                                  name='Thread-Command-' + self.name())
      thread.start()
      thread.joinWithTimeout(game.configurations.timeForCommand)
      if thread.isExpired():
        endTime = time.clock()
        self.durationTime = endTime - startTime
        raise errors.TimeoutCommandError(self)
    except errors.CommandError: raise
    except Exception, e:
      raise errors.BuggedCommandError(self, str(e))
    finally:
      endTime = time.clock()
      self.durationTime = endTime - startTime
      
class PlayerCommand(GameCommand):
  '''
  Example of usage:
  
  from gameengine import game
  
  class MyCommand(commands.PlayerCommand):

    def validate(self, context):
      # Must return InvalidCommandError if this command cant be executed in that context
      if context.flag == True: 
        raise InvalidCommandError(self, 'flag must be False!')
        raise CheatCommandError(self, 'ooops, invalid data')
    
    def executeWithValidation(self, game):
      # some implementation here, example:
      game.banPlayer(self.player)
  '''
  def __init__(self, player, params=None):
    super(PlayerCommand, self).__init__()
    self.player = player
    self.params = params
    
  def summary(self):
    params = '---'
    if self.params is not None: params = self.params
    t = Template('${command}, ${player}, ${params} - ${durationTime}s')
    return t.substitute(
                 command=self.name(), 
                 player=self.player, 
                 params=params,
                 durationTime=self.durationTime)

  def isValid(self, context):
    try:
      self.validate(context)
    except: return False
    else: return True
    
  def validate(self, context):
    '''
    raise an InvalidCommandError if an error occur
    '''
    pass
  
  def execute(self, game):
    self.validate(self.player.context)
    self.executeWithValidation(game)
    
  def executeWithValidation(self, game):
    raise NotImplementedError()
  
# Invoker of Command pattern.
# Client: Player-Strategy
# Receiver: Game
class CommandsManager(object):
  '''
  Invoke GameCommand commands.
  '''
  
  def __init__(self, game=None):
    self.game = game
    self.executedCommands = []
    self.validCommands = []
    
  def registerCommand(self, commandClass):
    self.validCommands.append(commandClass)
    
  def validateRegisteredCommand(self, command):
    if command.__class__ not in self.validCommands: 
      raise errors.UnknownCommandError(command)
    
  def start(self): pass
  def stop(self): pass
    
  def addCommand(self, command):
    pass
    
  def executeCommand(self, command):
    logger.debug('Executing command: ' + command.summary())
    self.game.permission.acquire()
    self.validateRegisteredCommand(command)
    command.process(self.game)
    self.game.notifyExecutedCommand(command)
    self.game.permission.release()
    self.executedCommands.append(command)
    logger.info('> ' + command.summary())
    if isinstance(command, PlayerCommand):
      logger.info(command.player.context.summary())
        
class SynchronousCommandsManager(CommandsManager):
  '''
  This class execute commands synchronously.
  
  Command: (player, params)
  '''
  
  def addCommand(self, command):
    self.executeCommand(command)

class AsynchronousCommandsManager(utils.AsyncQueueManager, CommandsManager):
  '''
  A thread runs asynchronously and enqueue commands and execute them synchronously.
  
  Command: (player, params)
  '''

  def __init__(self, game=None):
    utils.AsyncQueueManager.__init__(self, 'Thread-CommandsManager')
    CommandsManager.__init__(self, game)
  
  # Productor
  def addCommand(self, command):
    self.pushEvent(command)
  
  def processEvent(self, event):
    self.executeCommand(event)
    
