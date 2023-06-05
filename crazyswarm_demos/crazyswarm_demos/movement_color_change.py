import numpy as np
from crazyflie_py import *
from tkinter import *
from tkinter import colorchooser
import threading
import time

swarm = Crazyswarm()
timeHelper = swarm.timeHelper
allcfs = swarm.allcfs

Z = 1.0
allcfs.takeoff(targetHeight=Z, duration=1.0+Z)
timeHelper.sleep(1.5+Z)
for cf in allcfs.crazyflies:
    pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
    cf.goTo(pos, 0, 1.0)


def change_color():
    print("Press Enter to continue...")
    user_input = input()  # Wait for Enter key press

    if user_input == "":
        
        def chooser_color(): 
                color_code = colorchooser.askcolor(title="Choose color")
                r = color_code[0][0]
                g = color_code[0][1]
                b = color_code[0][2]
                for cf in allcfs.crazyflies:
                    cf.setLEDColor(r=r, g=g, b=b)
        
        def chooser_color_by_cf():
            for cf in allcfs.crazyflies:
                color_code = colorchooser.askcolor(title="Choose color")
                r = color_code[0][0]
                g = color_code[0][1]
                b = color_code[0][2]

                cf.setLEDColor(r=r, g=g, b=b)

        root = Tk()
        root.title("Pick the color combination!")
        button = Button(root, text = "Select color", command = chooser_color)
        button_led_for_each_cf = Button(root, text="Choose Color by CF", command = chooser_color_by_cf)
        button_led_for_each_cf.pack()
        button.pack()

        root.geometry("300x300")
        root.mainloop()
    
    else:
        print("Invalid input!")
        timeHelper.sleep(2.0)

        allcfs.land(targetHeight=0.02, duration=1.0+Z)
        timeHelper.sleep(1.0+Z)

def movement():
    start_time = time.time()
    while time.time() - start_time <= 30:
        for cf in allcfs.crazyflies:
            pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
            pos = pos + np.array([-1,0,0])
            cf.goTo(pos, 0, 5)
        timeHelper.sleep(5)
        for cf in allcfs.crazyflies:
            pos = pos + np.array([1,0,0])
            cf.goTo(pos, 0, 5)
        timeHelper.sleep(5)
    allcfs.land(targetHeight=0.02, duration=1.0+Z)
    timeHelper.sleep(1.0+Z)


def main():
    color_thread = threading.Thread(target=change_color)
    movement_thread = threading.Thread(target=movement)
    
    color_thread.start()
    movement_thread.start()

    color_thread.join()
    movement_thread.join()



if __name__ == "__main__":
    main()