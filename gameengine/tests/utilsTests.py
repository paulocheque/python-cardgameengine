'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import threading, time
import unittest
from gameengine import utils

class ObserverTests(unittest.TestCase):
  
  def testRegisterUnregister(self):
    observable = utils.Observable()
    observer1 = utils.Observer()
    observer2 = utils.Observer()
    observable.registerObserver(observer1)
    self.assertEquals(1, len(observable.observers))
    self.assertEquals(observer1, observable.observers[0])
    observable.registerObserver(observer2)
    self.assertEquals(2, len(observable.observers))
    self.assertEquals(observer1, observable.observers[0])
    self.assertEquals(observer2, observable.observers[1])
    observable.unregisterObserver(observer1)
    self.assertEquals(observer2, observable.observers[0])
  
  def testNotify(self):
    class MyObs(utils.Observer):
      def __init__(self):
        self.x = 1
      def notify(self, event):
        self.x = 5
    observable = utils.Observable()
    observer1 = MyObs()
    observer2 = MyObs()
    observable.registerObserver(observer1)
    observable.registerObserver(observer2)
    observable.notifyObservers(None)
    self.assertEquals(5, observer1.x)
    self.assertEquals(5, observer2.x)

###############################################################################

class CombinationGeneratorTests(unittest.TestCase):

  def test1Choose1(self):
    self.assertEquals([0], utils.CombinationGenerator(1, 1).next())
    
  def testNChooseN(self):
    self.assertEquals([0, 1, 2], utils.CombinationGenerator(3, 3).next())
  
  def test2Choose1(self):
    generator = utils.CombinationGenerator(2, 1)
    self.assertEquals([0], generator.next())
    self.assertEquals([1], generator.next())
    
  def test3Choose1(self):
    generator = utils.CombinationGenerator(3, 1)
    self.assertEquals([0], generator.next())
    self.assertEquals([1], generator.next())
    self.assertEquals([2], generator.next())
    
  def test3Choose2(self):
    generator = utils.CombinationGenerator(3, 2)
    self.assertEquals([0, 1], generator.next())
    self.assertEquals([0, 2], generator.next())
    self.assertEquals([1, 2], generator.next())
    
  def test4Choose3(self):
    generator = utils.CombinationGenerator(4, 3)
    self.assertEquals([0, 1, 2], generator.next())
    self.assertEquals([0, 1, 3], generator.next())
    self.assertEquals([0, 2, 3], generator.next())
    self.assertEquals([1, 2, 3], generator.next())
    
  def test4Choose2(self):
    generator = utils.CombinationGenerator(4, 2)
    self.assertEquals([0, 1], generator.next())
    self.assertEquals([0, 2], generator.next())
    self.assertEquals([0, 3], generator.next())
    self.assertEquals([1, 2], generator.next())
    self.assertEquals([1, 3], generator.next())
    self.assertEquals([2, 3], generator.next())
    
  def test5Choose3(self):
    generator = utils.CombinationGenerator(5, 3)
    self.assertEquals([0, 1, 2], generator.next())
    self.assertEquals([0, 1, 3], generator.next())
    self.assertEquals([0, 1, 4], generator.next())
    self.assertEquals([0, 2, 3], generator.next())
    self.assertEquals([0, 2, 4], generator.next())
    self.assertEquals([0, 3, 4], generator.next())
    self.assertEquals([1, 2, 3], generator.next())
    self.assertEquals([1, 2, 4], generator.next())
    self.assertEquals([1, 3, 4], generator.next())
    self.assertEquals([2, 3, 4], generator.next())

  def testSanity15Escolhe4(self):
    generator = utils.CombinationGenerator(15, 4)
    for x in range(30):
      combination = generator.next()
      self.assertEquals(4, len(combination))
      for y in combination:
        self.assertTrue(y >= 0 and y < 15)
  
  def testSanity50Escolhe7(self):
    generator = utils.CombinationGenerator(50, 7)
    for x in range(100):
      combination = generator.next()
      self.assertEquals(7, len(combination))
      for y in combination:
        self.assertTrue(y >= 0 and y < 50)
        
  def testPerformance(self):
    n = 16 # Java Rosen algorithm 22 in 1 second
    for r in range(1, n+1):
      generator = utils.CombinationGenerator(n, r)
      while generator.hasNext(): indexes = generator.next()
    
        
  def testAfterLastCombinationRestart(self):
    generator = utils.CombinationGenerator(3, 2)
    self.assertEquals([0, 1], generator.next())
    self.assertEquals([0, 2], generator.next())
    self.assertEquals([1, 2], generator.next())
    self.assertEquals([0, 1], generator.next())
    
  def testHasNext(self):
    generator = utils.CombinationGenerator(3, 2)
    self.assertTrue(generator.hasNext())
    generator.next()
    self.assertTrue(generator.hasNext())
    generator.next()
    self.assertTrue(generator.hasNext())
    generator.next()
    
    self.assertFalse(generator.hasNext())
    generator.next()
    self.assertTrue(generator.hasNext())
    
  def testReset(self):
    generator = utils.CombinationGenerator(3, 2)
    self.assertEquals([0, 1], generator.next())
    generator.reset()
    self.assertEquals([0, 1], generator.next())
    
  def testFactorial(self):
    generator = utils.CombinationGenerator(1, 1)
    self.assertEquals(1, generator.factorial(0))
    self.assertEquals(1, generator.factorial(1))
    self.assertEquals(2, generator.factorial(2))
    self.assertEquals(6, generator.factorial(3))
    self.assertEquals(3628800, generator.factorial(10))
    print(generator.factorial(50))
    print(generator.factorial(100))
  
###############################################################################

class AsyncQueueManagerTests(unittest.TestCase):
  
  def setUp(self):
    self.qm = utils.AsyncQueueManager('Thread-X')
    self.threads = threading.activeCount()
    
  def tearDown(self):
    self.qm.stop()
    while threading.activeCount() != self.threads:
      time.sleep(0.1)
  
  def testPushPop(self):
    self.assertEquals(0, self.qm.queueHeight())
    self.qm.pushEvent('event')
    self.assertEquals(1, self.qm.queueHeight())
    self.qm.popEvent()
    self.assertEquals(0, self.qm.queueHeight())

  def testStartStop(self):
    self.qm.stop()
    self.qm.stop()
    threads = threading.activeCount()
    self.qm.start()
    self.assertEquals(threads + 1, threading.activeCount())
    self.qm.stop()
    while threading.activeCount() != self.threads:
      time.sleep(0.1)
    self.assertEquals(threads, threading.activeCount())
    self.qm.stop()
    self.qm.stop()
    
  def testAddEventsBeforeStart(self):
    self.qm.pushEvent('event')
    self.assertEquals(1, self.qm.queueHeight())
    self.qm.start()
    time.sleep(0.1)
    self.assertEquals(0, self.qm.queueHeight())
    
  def testAddEventsBeforeStart2(self):
    self.qm.pushEvent('event')
    self.qm.pushEvent('event')
    self.assertEquals(2, self.qm.queueHeight())
    self.qm.start()
    time.sleep(0.2)
    self.assertEquals(0, self.qm.queueHeight())
  
  def testAddEventsAfterStart(self):
    self.qm.start()
    self.qm.pushEvent('event')
    self.assertEquals(1, self.qm.queueHeight())
    time.sleep(0.1)
    self.assertEquals(0, self.qm.queueHeight())
    
  def testAddEventsAfterStart2(self):
    self.qm.start()
    self.qm.pushEvent('event')
    self.qm.pushEvent('event')
    self.assertEquals(2, self.qm.queueHeight())
    time.sleep(0.1)
    self.assertEquals(0, self.qm.queueHeight())
    
  def testAddEventsAfterStart2(self):
    self.qm.start()
    self.qm.processEvent = lambda x: time.sleep(0.5)
    self.qm.pushEvent('event')
    self.assertEquals(1, self.qm.queueHeight())
    time.sleep(0.5)
    self.assertEquals(0, self.qm.queueHeight())
    self.qm.pushEvent('event')
    self.assertEquals(1, self.qm.queueHeight())
    time.sleep(0.5)
    self.assertEquals(0, self.qm.queueHeight())
  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()