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
