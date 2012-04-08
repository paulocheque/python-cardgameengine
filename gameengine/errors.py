'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

from gameengine import utils

# Commands

class CommandError(utils.Error):
  'Command error'
  
  def __init__(self, command, extra_information=None):
    if extra_information is not None:
      super(CommandError, self).__init__(command.summary() + ' - ' + extra_information)
    else:
      super(CommandError, self).__init__(command.summary())
  
class UnknownCommandError(CommandError):
  'Command not registered in commands manager: commandsManager.registerCommand(FooCommand)'
  
class InvalidCommandError(CommandError):
  'Algorithm try to execute an illegal command, against the rules'
  
class CheatCommandError(InvalidCommandError):
  'Algorithm try to execute an illegal and bad intentioned command, against the rules'
  
class BuggedCommandError(CommandError):
  'Command bugged'
  
class TimeoutCommandError(CommandError):
  'Command timeout: server busy or bad implementation'

# Commands Manager

class ExecutionError(utils.Error):
  'Tentative to start a started execution or tentative to stop a unstarted execution'

# Player Strategies

class MailiciousStrategyError(utils.Error):
  '''Algorithm try to execute a malicious command: It is forbidden import modules or use exec or eval functions'''

#  '''
#  Cheat: player algorithm can access only accessible informations, 
#  if he(she) try to get game informations he(she) is cheater.
#  Detecting cheat: algorithm contains string 'commandsManager.game'
#  def play(self, commandsManager):
#  '''
class CheatStrategyError(utils.Error):
  '''Algorithm try to execute a cheat command: It is forbidden to use the reserved term 'game'''

class TimeoutStrategyError(utils.Error):
  '''Strategy timeout: Algorithm is too slow, bugged or has some kind of infinite loop or some cycle strategy'''
  
# Game
  
class TimeoutGameError(utils.Error):
  '''Game timeout: Strategies are not ofensive or some kind of infinite loop or some cycle strategy'''
  