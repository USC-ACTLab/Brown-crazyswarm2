# import numpy as np
# from crazyflie_py import *
# from tkinter import *
# from tkinter import colorchooser
# import sounddevice as sd
# from matplotlib import colors
# import time as lib_time

# def main():
#     swarm = Crazyswarm()
#     timeHelper = swarm.timeHelper
#     allcfs = swarm.allcfs

#     sample_rate = 44100
#     chunk_size = 1024

#     color_map = colors.LinearSegmentedColormap.from_list('Spectrum', ['red', 'green', 'blue'])

#     def change_color(indata, frames, time, status):
#         amplitude = np.abs(indata).mean()
#         normalized_amplitude = amplitude / 1.0
#         threshold = 0.01

#         if normalized_amplitude <= threshold:
#             color = color_map(normalized_amplitude / threshold)
#         else:
#             color = color_map((normalized_amplitude - threshold) / (1 - threshold))

#         r, g, b, _ = color

#         r = int(r * 255)
#         g = int(g * 255)
#         b = int(b * 255)
#         for cf in allcfs.crazyflies:
#                 cf.setLEDColor(r=r, g=g, b=b)
        
#         timeHelper.sleepForRate(3.0)
#     # allcfs.takeoff(1.0, 2.5)

#     stream = sd.InputStream(callback=change_color, channels=1, samplerate=sample_rate, blocksize=chunk_size)
#     stream.start()

#     input("Press Enter to stop...")
#     stream.stop()
#     stream.close()
#     # allcfs.land(0.0, 2.5)
#     # timeHelper.sleep(2.5)

# if __name__ == "__main__":
#     main()







import numpy as np
from crazyflie_py import *
from tkinter import *
from tkinter import colorchooser
import sounddevice as sd
from matplotlib import colors
import time as lib_time


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    sample_rate = 44100
    chunk_size = 1024

    color_map = colors.LinearSegmentedColormap.from_list('Spectrum', ['red', 'green', 'blue'])

    def change_color(indata, frames, time, status):
        amplitude = np.abs(indata).mean()
        normalized_amplitude = amplitude / 1.0
        threshold = 0.01

        if normalized_amplitude <= threshold:
            color = color_map(normalized_amplitude / threshold)
        else:
            color = color_map((normalized_amplitude - threshold) / (1 - threshold))

        r, g, b, _ = color

        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        for cf in allcfs.crazyflies:
                cf.setLEDColor(r=r, g=g, b=b)
        
        timeHelper.sleepForRate(3.0)
    # allcfs.takeoff(1.0, 2.5)

    stream = sd.InputStream(callback=change_color, channels=1, samplerate=sample_rate, blocksize=chunk_size)
    stream.start()

    input("Press Enter to stop...")
    stream.stop()
    stream.close()
    # allcfs.land(0.0, 2.5)
    # timeHelper.sleep(2.5)

if __name__ == "__main__":
    main()