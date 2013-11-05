#!/usr/bin/env python

# Run n-1 threads from root raspi and see if you can synchronize       #
# all n-1 raspis to within 100 ms. NOTE as this is run on either a     #
# dedicated raspi or a desktop, we are not concerned with performance. #

import sys
import os
import threading
import time
import random
import subprocess

class RaspiSSh ( threading.Thread ):
   def __init__ ( self, ipaddress='', targetTime=-1, videoPath='', output=None, timeToRun=5, threadSleepTime=1 ):
      threading.Thread.__init__ ( self )
      
      self.ipaddress = ipaddress
      self.sshProcess = None
      self.sshCommand =  'ssh -t -t %s "/home/raspi/documents/coding/omxplayer-sync-tests/omxplayer-sync-tests/omxplayer-sync-tests.sh %d %s"' % ( ipaddress, targetTime, videoPath )
      self.timeToRun = timeToRun
      self.threadSleepTime = threadSleepTime
      self.output = output
   def run ( self ):
      self.sshProcess = subprocess.Popen ( self.sshCommand, stdout = subprocess.PIPE, stdin=subprocess.PIPE, shell = True)
      startTime = time.time()
      
      while ( self.sshProcess.poll () is None ):
         time.sleep( self.threadSleepTime )
         if time.time () - startTime > self.timeToRun:
            # Send signal to stop video (Ctr+C)
            try:
               self.stop ()
               self.sshProcess.wait ()
               self.output.append ( self.sshProcess.returncode )
               break
            except:
               print 'this is where the problem is'
   def stop ( self ):
      if  self.sshProcess.poll () is None:
         self.sshProcess.stdin.write ( 'q' )
      else:
         print 'asked to stop but Poll is not None'
   def formatOutput ( self ):
      print self.ipaddress
      print self.output
      total = 0.0
      for s in self.output:
         total += s
      print total / len ( self.output )

# The ip address of the raspis. NOTE I have raspis defined in my       #
# /etc/hosts file therefore I ssh them by name. Also, it goes without  #
# saying that you need keyless ssh enable.                             #
raspiIps = [ 'raspi1', 'raspi2' ]

# Path of movie to be synchronized (NOTE change this)
videoPath = '/home/raspi/media/video/movies/Idiocracy.2006.HDTV.720p.x264-HDL_25fps.mkv'
raspiserver = 'main'
numberOfTrials = 10
# number of miliseconds before launching omxplayer
def getTargetTime ( targetTime = 1 ):
   return targetTime * 1000


if __name__ == '__main__':
   for timeInFuture in [ 1, 2, 4, 5 ]:
      for movieTime in [ 4, 6]:
         for threadSleepTime in [ 0.1, 0.5, 1.0, 2.0 ]:
            # Remember to manually define output = [], if set to       #
            # default params in the class, the list will become        #
            # immutable and will be shared amongst both threads        #
            # resulting in super long output lists.                    #
            raspis = [ RaspiSSh( output = [] ), RaspiSSh( output = [] ) ]

            for j in range ( numberOfTrials ):
               targetTime = getTargetTime ( timeInFuture )
               curTime = time.time()
               for i, raspiIp in enumerate ( raspiIps ):
                  raspis [ i ] = RaspiSSh ( raspiIp, targetTime + curTime, videoPath, raspis [ i ].output, movieTime, threadSleepTime )
               try:
                  for raspi in raspis:
                     raspi.start ()
                     
                  for raspi in raspis:
                     raspi.join ()
               except:
                  for raspi in raspis:
                     raspi.stop ()
                  raise Exception
            print ""
            print "targetTime=%dms movieTime=%dms threadSleepTime=%.3fms scriptSleepTime=1000ms numberOfTrials=%d" % ( timeInFuture * 1000, movieTime, threadSleepTime, numberOfTrials )
            for raspi in raspis:
               raspi.formatOutput ()
