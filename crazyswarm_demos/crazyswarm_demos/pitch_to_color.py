import sounddevice as sd
from scipy.fftpack import fft
import sys
import numpy as np
import time as tm
from matplotlib import colors, pyplot as plt
from crazyflie_py import *
from tkinter import *
from tkinter import colorchooser

color_map = colors.LinearSegmentedColormap.from_list('Spectrum', ['red', 'green', 'blue'])

fz = []
blocksize = 2048

swarm = Crazyswarm()
timeHelper = swarm.timeHelper
allcfs = swarm.allcfs

def process_microphone_input(indata, frames, time, status):

    input_signal = indata[:, 0]  
    freq_domain = fft(input_signal)
    f = np.max(np.abs(freq_domain))

    frequency = f * sample_rate / blocksize
    fz.append(frequency)
    print_color_spectrum(frequency)

    # tm.sleep(0.2)
    

def print_color_spectrum(hz):


    if hz < 60:
        print(f"RGB: ({255}, {0}, {0})")
        return
    if hz > 660:
        print(f"RGB: ({0}, {0}, {255})")
        return

    color_map = colors.LinearSegmentedColormap.from_list('Spectrum', ['red', 'green', 'blue'])
    norm_number = (hz - 60) / (660 - 60)  # Normalize the number between 0 and 1

    rgb = color_map(norm_number)[:3]  # Extract RGB values and ignore the alpha channel

    red = int(rgb[0] * 255)
    green = int(rgb[1] * 255)
    blue = int(rgb[2] * 255)

    print(f"RGB: ({red}, {green}, {blue})")
    
    for cf in allcfs.crazyflies:
                cf.setLEDColor(r=red, g=green, b=blue) 
    timeHelper.sleepForRate(20)   

def microphone_pitch_detection():
    global sample_rate
    sample_rate = 44100  # Sample rate of the audio input

    # Start streaming audio from the microphone
    print("Listening...")
    tm.sleep(1)
    with sd.InputStream(callback=process_microphone_input, channels=1, samplerate=sample_rate, blocksize=blocksize):
        while True:
            user_input = input("Press Enter to exit: ")
            if user_input == "":
                # filtered_array = [x for x in fz if x <= 1000]
                # plt.plot(filtered_array)
                # plt.show()
                break
            pass
            
microphone_pitch_detection()