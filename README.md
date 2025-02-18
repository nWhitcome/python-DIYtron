# Python DIYtron
This repo is part of my ongoing effort to explore different ways that I can build a cross-platform, low latency emulation of a Mellotron.

It uses FluidSynth to play a .sf2 file that I generated from a sample library uploaded by Taijiguy taken from an old Mellotron. I updated and used the pyfluidsynth library to interact with it but have hit some roadblocks due to the way that FluidSynth operates.

I used Flask to create a local web server that would manage the front end of the program, hopefully to be used with something like Electron.

##Problems
I have managed to get FluidSynth to play all of the sounds I want in real time and to manipulate reverb settings but implementing attack and decay time is more difficult. There are functions for 'generators' that should make this easy, but the attack/decay time resets to whatever value is in the .sf2 file every time it plays a note, so they need to be called right after a key is pressed. This is incredibly annoying and inefficient and when combined with audio artifacts when changing reverb values in real time it seems like this might be a dead end.
