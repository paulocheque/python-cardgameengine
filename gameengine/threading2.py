'''
@author: 
http://sebulba.wikispaces.com/recipe+thread2
http://www.velocityreviews.com/forums/t330554-kill-a-thread-in-python.html
http://docs.python.org/library/threading.html
'''

import threading
import sys
import trace
#
class KThread(threading.Thread):
  """A subclass of threading.Thread, with a kill() method."""
  
  def __init__(self, *args, **keywords):
    threading.Thread.__init__(self, *args, **keywords)
    self.killed = False
    self.expired = False
    self.__exception = None

  def start(self):
    """Start the thread."""
    self.__run_backup = self.run
    self.run = self.__run # Force the Thread to install our trace.
    threading.Thread.start(self)
    
  def joinWithTimeout(self, timeout):
    # Wait for timeout seconds to the thread terminates
    if timeout < 0: self.join()
    else: self.join(timeout)
    if self.isAlive():
      self.expired = True
      self.kill()
      # Join waits until the thread terminates.
      self.join()
    if self.__exception is not None:
      raise self.__exception
      
  def isExpired(self):
    return self.expired

  def __run(self):
    """Hacked run function, which installs the trace."""
    try:
      sys.settrace(self.globaltrace)
      self.__run_backup()
      self.run = self.__run_backup
    except Exception, e:
      e.message = e.__class__.__name__ + ' in ' + self.getName() + ': ' + e.message
      self.__exception = e
  
  def globaltrace(self, frame, why, arg):
    if why == 'call':
      return self.localtrace
    else:
      return None

  def localtrace(self, frame, why, arg):
    if self.killed:
      if why == 'line':
        raise SystemExit()
    return self.localtrace # identation correct?

  def kill(self):
    self.killed = True
    
#import threading
#import inspect
#import ctypes
# 
#def _async_raise(tid, exctype):
#    """raises the exception, performs cleanup if needed"""
#    if not inspect.isclass(exctype):
#        raise TypeError("Only types can be raised (not instances)")
#    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
#    if res == 0:
#        raise ValueError("invalid thread id")
#    elif res != 1:
#        # """if it returns a number greater than one, you're in trouble, 
#        # and you should call it again with exc=NULL to revert the effect"""
#        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
#        raise SystemError("PyThreadState_SetAsyncExc failed")
# 
# 
#class Thread(threading.Thread):
#    def _get_my_tid(self):
#        """determines this (self's) thread id"""
#        if not self.isAlive():
#            raise threading.ThreadError("the thread is not active")
# 
#        # do we have it cached?
#        if hasattr(self, "_thread_id"):
#            return self._thread_id
# 
#        # no, look for it in the _active dict
#        for tid, tobj in threading._active.items():
#            if tobj is self:
#                self._thread_id = tid
#                return tid
# 
#        raise AssertionError("could not determine the thread's id")
# 
#    def raise_exc(self, exctype):
#        """raises the given exception type in the context of this thread"""
#        _async_raise(self._get_my_tid(), exctype)
# 
#    def terminate(self):
#        """raises SystemExit in the context of the given thread, which should 
#        cause the thread to exit silently (unless caught)"""
#        self.raise_exc(SystemExit)

#class StoppableThread (threading.Thread):
#  """Thread class with a stop() method. The thread itself has to check regularly for the stopped() condition."""
#
#  def __init__ (self):
#    super(StoppableThread, self).__init__()
#    self._stop = threading.Event()
#  
#  def stop (self):
#    self._stop.set()
#  
#  def stopped (self):
#    return self._stop.isSet()

