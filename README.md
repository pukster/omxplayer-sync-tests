omxplayer-sync-tests
====================

A series of tests to determine if it is possible to somehow launch
multiple instances of omxplayer on n raspis with minimal (< 100ms)
difference between playtime.

There are currently, to the best of the this author's knowledge, two
projects which attempt to synchronize video, vlc for raspi (ported by
Helder Araujo Carneiro) and turingmachine/omxplayer-sync, as well as
streaming methods such as udp and http.

The hardware accelerated VLC distribution is a nightmare to build on
the raspi as the raspi is so slow. Cross compilation would alleviate
this problem, but that too is not for novice to intermediate users.
Furthermore, once built, there is no guarantee that it will work at
all as libraries may need to be properly linked. Finally, even if it
does work, the raspi has to be overclocked as it is not as efficient as
omxplayer. There is a precompiled version which Helder has conveniently
provided (thanks!), however, there is no guarantee that it will look
for the libraries in the correct places you have installed them. Novice
to intermediate users will again struggle to figure out how to find the
locations that omxplayer-sync is looking in and start spamming symbolic
links all over the place.

omxplayer-sync is exactly what this author is looking for: the ability
to synchronize multiple raspi instances of omxplayer. Unfortunately, it
uses python to launch multiple threads/processes, and then constantly
loops to check for deviations in timing. This constant python
interpretter causes serious performance issues as even 720p video begins
to lag.

This author has also tested some, but definitely not all, streaming
options using vlc on a desktop (read 'not total piece of raspi garbage),
however, when the stream is opened on the target raspi, it looks like a
total piece of garbage. The auther is not alone here either, however, he
will admit that this may be because he simply does not know what he is
doing with respect to streams.

The approach take here will be different in that the different raspis
will synchronized first THEN omxplayer will be launched. The tests I am
looking to run include: 

1) Set a target start time in milliseconds since epoch and see if the
raspis can launch by that target within 100ms or less.

2) Visually and acoustically determine whether the differences are
manageable.
   I found that the differences were noticeable, however, if only       
   one audio source is used, then the difference is not noticeable.     
   Numerically,                                                         

3) Determine how near in the future we can put the target launch time
without worrying about the time needed to launch all threads and issue
all ssh commands

4) Run a quick movie (ie. 0.5 s) to test not only when the omxplayer
command is issued, but also when the omxplayer terminates. This will
give a better idea of how similar the two time windows are.

There is an alternative to this, which would be to modify the omxplayer
source code, provide a target time, and do the time processing in C.
This would be a much better solution. However, if this works, I would
much rather use this as building omxplayer could be a major disaster,
especially if I have to rebuild ffmpeg.

PROBLEMS

   I noticed a slight problem in the programming where certain movies
   would play for slightly longer than they should have, even though one
   of the raspis had already received the 'q' signal to exit.

   I noticed the program sometimes crashed when movie times were too
   short (< 2 s)

   The program gets to a point where the threads deadlock and I can't figure
   out why. Quite frankly i don't have the time either.

RESULTS

Here are the results I got for the different values, where

targetTime is how far into the future wait before launching shell script

movieTime is how long to run movie for

threadSleepTime is how long to wait before checking if movieTime has
expired

scriptSleepTime is how long to wait before checking if targetTime has
been achieved

numberOfTrials is the number of times the above is iterated

targetTime=1000ms movieTime=4ms threadSleepTime=0.100ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[0, 32, 46, 54, 28, 41, 84, 84, 91, 137]
59.7
raspi2
[222, 122, 206, 158, 105, 135, 207, 223, 189, 214]
178.1

targetTime=1000ms movieTime=4ms threadSleepTime=0.500ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[137, 129, 140, 183, 199, 207, 81, 148, 172, 232]
162.8
raspi2
[213, 207, 228, 246, 29, 37, 48, 63, 11, 95]
117.7

targetTime=1000ms movieTime=4ms threadSleepTime=1.000ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[186, 226, 221, 232, 220, 213, 238, 228, 234, 238]
223.6
raspi2
[34, 92, 65, 63, 37, 50, 49, 57, 69, 61]
57.7

targetTime=1000ms movieTime=4ms threadSleepTime=2.000ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[239, 144, 201, 191, 205, 52, 148, 178, 202, 181]
174.1
raspi2
[87, 79, 33, 29, 88, 17, 235, 232, 5, 80]
88.5

targetTime=1000ms movieTime=6ms threadSleepTime=0.100ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[186, 142, 156, 128, 138, 71, 81, 64, 35, 30]
103.1
raspi2
[61, 238, 234, 225, 202, 178, 166, 161, 178, 83]
172.6

targetTime=1000ms movieTime=6ms threadSleepTime=0.500ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[136, 195, 152, 131, 137, 199, 173, 121, 129, 60]
143.3
raspi2
[62, 40, 249, 218, 199, 14, 64, 220, 185, 144]
139.5

targetTime=1000ms movieTime=6ms threadSleepTime=1.000ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[38, 28, 21, 241, 155, 131, 107, 30, 36, 238]
102.5
raspi2
[144, 186, 144, 105, 247, 34, 175, 218, 82, 77]
141.2

targetTime=1000ms movieTime=6ms threadSleepTime=2.000ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[236, 8, 42, 197, 216, 160, 108, 113, 52, 109]
124.1
raspi2
[102, 22, 160, 121, 85, 47, 15, 223, 198, 129]
110.2

targetTime=2000ms movieTime=4ms threadSleepTime=0.100ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[134, 162, 184, 124, 199, 212, 190, 245, 1, 14]
146.5
raspi2
[31, 37, 54, 231, 60, 77, 29, 102, 134, 129]
88.4

targetTime=2000ms movieTime=4ms threadSleepTime=0.500ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[4, 15, 26, 76, 117, 122, 146, 149, 160, 234]
104.9
raspi2
[172, 179, 127, 230, 188, 247, 17, 43, 68, 101]
137.2

targetTime=2000ms movieTime=4ms threadSleepTime=1.000ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[232, 14, 248, 25, 55, 52, 94, 49, 97, 207]
107.3
raspi2
[97, 129, 148, 120, 210, 170, 225, 169, 221, 219]
170.8

targetTime=2000ms movieTime=4ms threadSleepTime=2.000ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[47, 30, 75, 21, 112, 61, 70, 247, 28, 39]
73.0
raspi2
[171, 181, 193, 177, 139, 146, 231, 94, 141, 156]
162.9

targetTime=2000ms movieTime=6ms threadSleepTime=0.100ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[45, 6, 16, 13, 216, 241, 173, 175, 184, 151]
122.0
raspi2
[171, 169, 137, 131, 109, 102, 28, 253, 55, 24]
117.9

targetTime=2000ms movieTime=6ms threadSleepTime=0.500ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[152, 132, 101, 51, 0, 240, 235, 201, 197, 133]
144.2
raspi2
[16, 250, 222, 206, 179, 116, 99, 87, 67, 254]
149.6

targetTime=2000ms movieTime=6ms threadSleepTime=1.000ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[120, 75, 15, 235, 184, 212, 203, 121, 94, 65]
132.4
raspi2
[246, 200, 182, 133, 109, 77, 66, 29, 13, 207]
126.2

targetTime=2000ms movieTime=6ms threadSleepTime=2.000ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[53, 247, 216, 213, 187, 177, 110, 85, 212, 69]
156.9
raspi2
[116, 157, 63, 89, 57, 48, 20, 225, 76, 187]
103.8

targetTime=4000ms movieTime=4ms threadSleepTime=0.100ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[22, 115, 113, 121, 147, 209, 231, 221, 40, 20]
123.9
raspi2
[196, 236, 23, 9, 219, 77, 107, 140, 162, 112]
128.1

targetTime=4000ms movieTime=4ms threadSleepTime=0.500ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[60, 78, 116, 70, 81, 133, 112, 176, 135, 99]
106.0
raspi2
[190, 210, 235, 224, 160, 250, 14, 50, 7, 204]
154.4

targetTime=4000ms movieTime=4ms threadSleepTime=1.000ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[115, 128, 78, 97, 141, 110, 116, 158, 136, 114]
119.3
raspi2
[200, 54, 245, 207, 10, 0, 202, 26, 15, 41]
100.0

targetTime=4000ms movieTime=4ms threadSleepTime=2.000ms scriptSleepTime=1000ms numberOfTrials=10
raspi1
[203, 223, 234, 244, 207, 173, 230, 221, 218, 246]
219.9
raspi2
[71, 76, 100, 142, 73, 74, 93, 80, 119, 146]
97.4

CONCLUSION
Bear in mind that both raspis are physically the same, and they are
running identical images, and using NFS for the omxplayer-sync-tests.sh
file. Therfore, optimizing the raspis will probably not yield better
results. Furthermore, a call to `top` indicates that the CPU is only 1%
used, and there are 63 jobs, with 62 of those sleeping.

This is not a suitable solution as the time differences from the desired
target time are not guaranteed to be < 100 ms. Although very often the
time difference between the raspis is <100ms the audio still has a
noticable time difference. This is taken to mean that although omxplayer
is called at near identical times, the video is loaded at different
times. What is instead needed here is launch omxplayers, pause them, and
then unpause them all together. This, however, requires modifying the
source code. As much as it pains me to say it, I will have to do that
next.
