

import numpy as np
from matplotlib import pyplot as plt
import pyaudio
#import msvcrt
import wave
import time
from serial import Serial
import socket
import OSC

def play_breath(audiopath):
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
    while data != '':
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)

    # cleanup stuff.
    stream.close()    
    p.terminate()

def microphone_data(usbserial='/dev/tty.usbserial-AL02A0KY', gender='woman'):
    speed='slow'
    exhaling=[]
    peaktopeak0=1
    
    ser= Serial(usbserial,9600) #timeout required for ser.readline()
    print "start"
    
    
    #osc_handling
    UDP_ADDRESS = '127.0.0.1', 5000
    c = OSC.OSCClient()
    c.connect(UDP_ADDRESS)
    msg = OSC.OSCMessage()
    msg.setAddress("/microphone")
    msg.append("start")
    c.send(msg)
    
    #while not msvcrt.kbhit(): #goes until key is pressed, change for mac
    while True:
        num=''
        for i in ser.readline():
            if i in '0123456789':
                num=num + i
        
        num=float(num)
        data = num
        sensor_data.append(num)
        
        if len(sensor_data)>1000:
            lower_quarter.append(np.percentile(sensor_data[-1000:],15))
        else:
            lower_quarter.append(np.percentile(sensor_data,15))
        peaktopeak=max(sensor_data[-70:])-np.min(sensor_data[-70:])

        peaktopeaklist.append(peaktopeak)
        gainlist.append(peaktopeak/peaktopeak0)
        msg.clearData()
        msg.append(gainlist[-1])
        c.send(msg)

        if num<lower_quarter[-1]: #if number lower than normal, this is exhale
            exhaling.append(time.time())
            if len(exhaling)==1 or exhaling[-2] < exhaling[-1]-1:
                exhalestart.append(exhaling[-1])
                peaktopeak0=peaktopeak
                msg.clearData()
                msg.append('start')
                c.send(msg)
                #print exhalestart
                #play_breath(gender+"_"+speed+".wav")
                if len(exhalestart)>=3: #calculate breaths per minute
                    bpm=60/np.average(np.diff(exhalestart[-3:])) #breaths per minute
                    if bpm>18:
                        speed='fast'
                    else:
                        speed='slow'

def temperature_data(usbserial='/dev/tty.usbserial-A402YQS2'):
    ser= Serial(usbserial,9600)

    #while not msvcrt.kbhit(): #goes until key is pressed, change for mac
    while True:
        #num=ser.readline()
        num=''
        for i in ser.readline():
            if i in '0123456789':
                num=num + i
        
        num=float(num)
        data = num
        sensor_data.append(num)
        print num


if __name__ == '__main__':

    sensor_data=[] #sensor data
    lower_quarter=[]  #sensor data baseline
    exhalestart=[] #exhale counts on time
    peaktopeaklist=[]
    gainlist=[]

        
    try:
        print "running!"
        #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

        microphone_data()
    #temperature_data()
    
    
    except KeyboardInterrupt:
        print "done"
    	print "total exhales: " + str(len(exhalestart))
    	print "average bpm: " + str(60/np.average(np.diff(exhalestart)))
    	plt.plot(sensor_data, 'k')
    	plt.plot(lower_quarter,'r')
    	plt.show()
        #ser._serial.close()

