'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import time
import threading
import unittest
from gameengine import threading2

class KThreadTests(unittest.TestCase):

  def setUp(self):
    self.thread = None
    
  def tearDown(self):
    if self.thread.isAlive():
      self.thread.kill()
      self.thread.join()
  
  def testKillKThread(self):
    spy = []
    def func(spy):
      time.sleep(0.3)
      spy.append(1)
      time.sleep(0.3)
      spy.append(2)
      time.sleep(0.3)
      spy.append(3)
      
    self.thread = threading2.KThread(target=func, args=[spy])
    numberOfThreads = threading.activeCount()
    self.thread.start()
    self.assertEquals(numberOfThreads + 1, threading.activeCount())
    self.assertTrue(self.thread.isAlive())
    self.thread.join(0.5)
    self.thread.kill()
    self.thread.join()
    self.assertEquals(numberOfThreads, threading.activeCount())
    self.assertFalse(self.thread.isAlive())
    self.assertTrue(len(spy) < 3)
    
  def testThreadWithTimeoutExpiring(self):
    spy = []
    def func(spy):
      time.sleep(0.3)
      spy.append(1)
      time.sleep(0.3)
      spy.append(2)
      time.sleep(0.3)
      spy.append(3)
    
    numberOfThreads = threading.activeCount()
    self.thread = threading2.KThread(target=func, args=[spy])
    self.thread.start()
    self.thread.joinWithTimeout(0.5)
    self.assertEquals(numberOfThreads, threading.activeCount())
    self.assertFalse(self.thread.isAlive())
    self.assertTrue(self.thread.isExpired())
    self.assertTrue(len(spy) < 3)
    
  def testThreadWithTimeoutWithoutExpiring(self):
    spy = []
    def func(spy):
      time.sleep(0.3)
      spy.append(1)
      time.sleep(0.3)
      spy.append(2)
      time.sleep(0.3)
      spy.append(3)
    
    numberOfThreads = threading.activeCount()
    self.thread = threading2.KThread(target=func, args=[spy])
    self.thread.start()
    self.thread.joinWithTimeout(1)
    self.assertEquals(numberOfThreads, threading.activeCount())
    self.assertFalse(self.thread.isAlive())
    self.assertFalse(self.thread.isExpired())
    self.assertTrue(len(spy) == 3)
    
  def testThreadWithTimeoutNegativaValueMustIgnoreTimeout(self):
    spy = []
    def func(spy):
      time.sleep(0.3)
      spy.append(1)
      time.sleep(0.3)
      spy.append(2)
      time.sleep(0.3)
      spy.append(3)
    
    spy = []
    numberOfThreads = threading.activeCount()
    self.thread = threading2.KThread(target=func, args=[spy])
    self.thread.start()
    self.thread.joinWithTimeout(-1)
    self.assertEquals(numberOfThreads, threading.activeCount())
    self.assertFalse(self.thread.isAlive())
    self.assertFalse(self.thread.isExpired())
    self.assertTrue(len(spy) == 3)
    
    
  def testKThreadMustRaiseAnExceptionToParentThreadIfOccurs(self):
    def func():
      raise Exception('some msg')
    self.thread = threading2.KThread(target=func, name='Thread-33')
    try:
      self.thread.start()
      self.thread.joinWithTimeout(-1)
    except Exception, e:
      self.assertEquals('Exception in Thread-33: some msg', e.message)
    else: self.fail()
    
  def testKThreadMustNotRaiseAnExceptionToParentThreadIfTimeoutExpired(self):
    def func():
      time.sleep(1)
    self.thread = threading2.KThread(target=func)
    try:
      self.thread.start()
      self.thread.joinWithTimeout(0.1)
    except Exception, e:
      self.fail()
    else: pass
    
  def testExceptionMessageMustHaveTypeAndThreadName(self):
    class MyException(Exception): pass
    def func():
      raise MyException('some msg')
    self.thread = threading2.KThread(target=func, name='Some Thread')
    try:
      self.thread.start()
      self.thread.joinWithTimeout(-1)
    except Exception, e:
      self.assertEquals('MyException in Some Thread: some msg', e.message)
      self.assertEquals('some msg', str(e))
    else:
      self.fail()
      
  def testThreadMustNotWaitUntilTheEndOfTimeoutIfThreadFinish(self):
    def func():
      time.sleep(0.1)
    self.thread = threading2.KThread(target=func, name='Some Thread')
    self.thread.daemon = True
    start = time.clock()
    self.thread.start()
    self.thread.joinWithTimeout(10000)
    end = time.clock()
    print(end - start)
    self.assertTrue(end - start < 1)
  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()