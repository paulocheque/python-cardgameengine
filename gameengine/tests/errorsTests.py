'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import time
import threading

import unittest

from gameengine import errors, testhelper

class ErrorsTest(testhelper.GameEngineTests):  
  
  def testMessageIsTheDoc(self):
    self.assertEquals(errors.InvalidCommandError.__doc__ + ': Neutral, Player1, --- - 0s', 
                      str(errors.InvalidCommandError(self.neutralcommand)))
    self.assertEquals(errors.UnknownCommandError.__doc__ + ': Neutral, Player1, --- - 0s',
                      str(errors.UnknownCommandError(self.neutralcommand)))
    
  def testErrorCanHaveExtraInformation(self):
    self.assertEquals(errors.ExecutionError.__doc__ + ': some info',
                      str(errors.ExecutionError('some info')))
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()