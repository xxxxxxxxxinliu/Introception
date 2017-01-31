import numpy as np
from matplotlib import pyplot as plt
import pyaudio
#import pykeyboard
#import msvcrt
import curses #mac keyboard
import wave
import time
import os
import sys

def exhale(gender, binsize=8192, rate=44100, threshold=7000):
#def exhale(gender, binsize=2**12, rate=48000, threshold=7000):
    win = curses.initscr()
    win.nodelay(True)
    key = win.getch()
    i = 0
    exhalestart=[] #list of all times that an exhale is audible
    exhaling=[] #list of start times of each exhale
    peaklist=[]
    speed= "slow"
    print "start"

    if i == 0:
        mp=pyaudio.PyAudio()
        mstream=mp.open(format=pyaudio.paInt16,channels=1,rate=rate,input=True,input_device_index = 0,frames_per_buffer=binsize)
        i = 1
    
    #while not msvcrt.kbhit():  #code runs until any key is pressed. this should change later when device's off/on mechanism is figured out
    #while True:
    while i == 1:
        mdata = np.fromstring(mstream.read(binsize),dtype=np.int16)
        #print(mdata)
        peak = np.average(np.abs(mdata))*2 #calculates average amplitude of each frequency
        peaklist.append(peak) #tracks the peaks
        if peak > threshold: 
            exhaling.append(time.time())
            if len(exhaling)==1 or exhaling[-2] < exhaling[-1]-1:
                exhalestart.append(exhaling[-1])
                play_breath(gender+"_"+speed+".wav")
                print "exhale"
                mstream.stop_stream()
                mstream.close()
                mp.terminate()
    if len(exhalestart)>=3: #calculate breaths per minute
        bpm=60/np.average(np.diff(exhalestart[-3:])) #breaths per minute
        if bpm>18:
            speed="fast"
        else:
            speed="slow"
        #if key != -1:
        print "done"
        print "total exhales: " + str(len(exhalestart))
        print "average bpm: " + str(60/np.average(np.diff(exhalestart)))


    ##plot data
    #plt.plot(peaklist)
    #plt.show()

def play_breath(audiopath):

    i = 0
    # length of data to read.
    chunk = 1024

    wf = wave.open(audiopath)
    # create an audio object
    p = pyaudio.PyAudio()
    # open stream based on the wave object which has been input.
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)

    # play stream (looping from beginning of file to the end)
    while len(data) > 0:
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)
        
    # cleanup stuff.
    
    stream.stop_stream()
    stream.close() 
    p.terminate()

if __name__=="__main__":
    exhale("woman")