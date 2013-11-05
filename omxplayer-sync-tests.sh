#!/bin/bash

# Raspberry Pi is, for the lack of a better term, a pice of shit. If   #
# You have an echo statement running in the background, omxplayer      #
# whill struggle with HD video. Therefore, synchronizing video will    #
# require starting at the same time, NOT having a program monitor its  #
# progress. For this reason, this simple script will sleep at 0.1ms    #
# intervals and check to see whether it should start or not.           #
if [ $# -lt 1 ]
then
   echo USAGE: ./omxplayer-sync-hack time [ omxplayer-command, ...]
   exit -1
fi

HOST=$(hostname)
curTime=$(($(date +%s%N)/1000000))
desiredTime=$1 # time to launch all raspis in synchrony
omxparams=''
i=0

# Do not pass all params in "$@" as the first parameter is the desired #
# time.                                                                #
for param in "$@"
do
   if [ $i != 0 ]
   then
      omxparams="$omxparams $param"
   fi
   i=$(($i+1))
done

# The leap of faith here is that `sleep 0.1` will work in some         #
# meaningful way.                                                      #
while [ $curTime -lt $desiredTime ]
do
   curTime=$(($(date +%s%N)/1000000))
   sleep 0.1
done

echo desired time: $desiredTime
echo actual time: $curTime
echo difference: $(($curTime-$desiredTime))

# Most of the time this script called from one of the raspis, however, #
# if called from main or the raspiserver, make sure not to call        #
# omxplayer as it is non existent                                      #
#                                                                      #
# NOTE change these machine names to fit your own set up               #
if [ $HOST != main ] && [ $HOST != raspiserver ]
then
   omxplayer $omxparams
fi

# Return the time difference to omxplayer-sync-test.py                 #
exit $(($curTime-$desiredTime))
