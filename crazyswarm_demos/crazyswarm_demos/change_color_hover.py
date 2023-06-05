import numpy as np
from crazyflie_py import *
from tkinter import *
from tkinter import colorchooser

def main():
    Z = 1.0
    
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.takeoff(targetHeight=Z, duration=1.0+Z)
    timeHelper.sleep(1.5+Z)
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        cf.goTo(pos, 0, 1.0)

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
        
            # root.destroy()

        def chooser_color_by_cf():
            for cf in allcfs.crazyflies:
                color_code = colorchooser.askcolor(title="Choose color")
                r = color_code[0][0]
                g = color_code[0][1]
                b = color_code[0][2]

                cf.setLEDColor(r=r, g=g, b=b)



        def stop():
            for cf in allcfs.crazyflies:
                cf.setLEDColor(r=0, g=0, b=0)
            allcfs.land(targetHeight=0.02, duration=1.0+Z)
            timeHelper.sleep(1.0+Z)
            root.destroy()
        

        root = Tk()
        root.title("Pick the color combination!")
        button = Button(root, text = "Select color", command = chooser_color)
        # button_exit = Button(root, text = "Exit", command = exit)
        button_stop = Button(root, text = "Terminate Flight", command = stop)
        button_led_for_each_cf = Button(root, text="Choose Color by CF", command = chooser_color_by_cf)

        button.pack()
        # button_exit.pack()
        button_led_for_each_cf.pack()
        button_stop.pack()
        root.geometry("300x300")
        root.mainloop()
    
    else:
        print("Invalid input!")
        timeHelper.sleep(2.0)

        allcfs.land(targetHeight=0.02, duration=1.0+Z)
        timeHelper.sleep(1.0+Z)

if __name__ == "__main__":
    main()