#!/usr/bin/env python

from midiutil import MIDIFile

scales = [
    [60, 62, 64, 65, 67, 69, 71, 72],  # MIDI note number
    [72, 71, 69, 67, 65, 64, 62, 60]  # MIDI note number
]

track = 0
channels = [0, 1]  # split into channels for parts
time = 0    # In beats
duration = 1    # In beats
tempo = 60   # In BPM
volume = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
# automatically)
MyMIDI.addTempo(track, time, tempo)

for channel in channels:
    for i, pitch in enumerate(scales[channel]):
        MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
