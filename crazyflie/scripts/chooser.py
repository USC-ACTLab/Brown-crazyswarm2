#!/usr/bin/env python3

import argparse
import copy
from functools import partial
from logging import root
try:
    import Tkinter
except ImportError:
    import tkinter as Tkinter
from ruamel.yaml import YAML
import pathlib
import os
import subprocess
import re
import time
import threading
from tkinter import *
from tkinter import colorchooser
import numpy as np
from crazyflie_py import *


def main():
    if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--configpath",
            type=str,
            default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "../config/crazyflies.yaml"),
            help="Path to the configuration .yaml file")
        parser.add_argument(
            "--stm32Fw",
            type=str,
            default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../../crazyflie-firmware/cf2.bin"),
            help="Path to cf2.bin")
        parser.add_argument(
            "--nrf51Fw",
            type=str,
            default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../../crazyflie2-nrf-firmware/cf2_nrf.bin"),
            help="Path to cf2_nrf.bin")
        args = parser.parse_args()

        if not os.path.exists(args.configpath):
            print("ERROR: Could not find yaml configuration file in configpath ({}).".format(args.configpath))
            exit()

        if not os.path.exists(args.stm32Fw):
            print("WARNING: Could not find STM32 firmware ({}).".format(args.stm32Fw))

        if not os.path.exists(args.nrf51Fw):
            print("WARNING: Could not find NRF51 firmware ({}).".format(args.nrf51Fw))

        def selected_cfs():
            nodes = {name: node for name, node in cfg["robots"].items() if widgets[name].checked.get()}
            return nodes

        def save():
            for name, node in cfg["robots"].items():
                if widgets[name].checked.get():
                    node["enabled"] = True
                else:
                    node["enabled"] = False
            with open(args.configpath, 'w') as outfile:
                yaml.dump(cfg, outfile)

        yaml = YAML()
        yaml.default_flow_style = True
        cfg = yaml.load(pathlib.Path(args.configpath))
        cfTypes = cfg["robot_types"]
        enabled = [name for name in cfg["robots"].keys() if cfg["robots"][name]["enabled"] == True]

        positions = [node["initial_position"] for node in cfg["robots"].values()]
        DOWN_DIR = [0, -1]
        RIGHT_DIR = [1, 0]
        def dot(a, b):
            return a[0] * b[0] + a[1] * b[1]
        pixel_x = [120 * dot(pos, RIGHT_DIR) for pos in positions]
        pixel_y = [120 * dot(pos, DOWN_DIR) for pos in positions]
        xmin, ymin = min(pixel_x), min(pixel_y)
        xmax, ymax = max(pixel_x), max(pixel_y)
        global top
        top = Tkinter.Tk()

        top.title('Crazyflie Chooser')

        # construct the frame containing the absolute-positioned checkboxes
        width = xmax - xmin + 200 # account for checkbox + text width
        height = ymax - ymin + 200 # account for checkbox + text height
        frame = Tkinter.Frame(top, width=width, height=height)

        class CFWidget(Tkinter.Frame):
            def __init__(self, parent, name):
                Tkinter.Frame.__init__(self, parent)
                self.checked = Tkinter.BooleanVar()
                checkbox = Tkinter.Checkbutton(self, variable=self.checked, command=save, padx=0, pady=0)
                checkbox.grid(row=0, column=0, sticky='e')

                nameLabel = Tkinter.Label(self, text=name, padx=0, pady=0, wraplength=150)
                nameLabel.grid(row=0, column=1, sticky='w')

                self.batteryLabel = Tkinter.Label(self, text="", fg="#999999", padx=0, pady=0)
                self.batteryLabel.grid(row=1, column=0, columnspan=2, sticky='e')

                self.versionLabel = Tkinter.Label(self, text="", fg="#999999", padx=0, pady=0)
                self.versionLabel.grid(row=2, column=0, columnspan=2, sticky='e')

                self.grid_columnconfigure(1, weight=1) 

        # construct all the checkboxes
        widgets = {}
        for (id, node), x, y in zip(cfg["robots"].items(), pixel_x, pixel_y):
            # w = CFWidget(frame, str(id) + '(' + str(x) + ',' + str(y) +')')
            print(id)
            w = CFWidget(frame, str(id))
            w.place(x = x - xmin, y = y - ymin)
            w.checked.set(id in enabled)
            widgets[id] = w
        

        # dragging functionality - TODO alt-drag to deselect
        drag_start = None
        drag_startstate = None

        def minmax(a, b):
            return min(a, b), max(a, b)

        def mouseDown(event):
            global drag_start, drag_startstate
            drag_start = (event.x_root, event.y_root)
            drag_startstate = [cf.checked.get() for cf in widgets.values()]

        def mouseUp(event):
            save()

        def drag(event, select):
            x, y = event.x_root, event.y_root
            dragx0, dragx1 = minmax(drag_start[0], x)
            dragy0, dragy1 = minmax(drag_start[1], y)

            def dragcontains(widget):
                x0 = widget.winfo_rootx()
                y0 = widget.winfo_rooty()
                x1 = x0 + widget.winfo_width()
                y1 = y0 + widget.winfo_height()
                return not (x0 > dragx1 or x1 < dragx0 or y0 > dragy1 or y1 < dragy0)

            # depending on interation over dicts being consistent
            for initial, cf in zip(drag_startstate, widgets.values()):
                if dragcontains(cf):
                    cf.checked.set(select)
                else:
                    cf.checked.set(initial)

        top.bind('<ButtonPress-1>', mouseDown)
        top.bind('<ButtonPress-3>', mouseDown)
        top.bind('<B1-Motion>', lambda event: drag(event, True))
        top.bind('<B3-Motion>', lambda event: drag(event, False))
        top.bind('<ButtonRelease-1>', mouseUp)
        top.bind('<ButtonRelease-3>', mouseUp)

        # buttons for clearing/filling all checkboxes
        def clear():
            for box in widgets.values():
                box.checked.set(False)
            save()

        def fill():
            for box in widgets.values():
                box.checked.set(True)
            save()

        def mkbutton(parent, name, command):
            button = Tkinter.Button(parent, text=name, command=command)
            button.pack(side='left')

        buttons = Tkinter.Frame(top)
        mkbutton(buttons, "Clear", clear)
        mkbutton(buttons, "Fill", fill)

        # construct bottom buttons for utility scripts
        def sysOff():
            nodes = selected_cfs()
            for name, crazyflie in nodes.items():
                uri = crazyflie["uri"]
                subprocess.call(["ros2 run crazyflie reboot --uri " + uri + " --mode sysoff"], shell=True)

        def change_positions():
            global drone_window
            root = Tk()
            root.title("test")
            root.withdraw()  
            drone_window = Toplevel(root)
            drone_window.title("Drone Inputs")


            def change_cf_position(name, cf, inputs):
                if len(inputs[0].get()) > 0 and len(inputs[0].get()) > 0 and len(inputs[0].get()) > 0:
                    cfg['robots'][name]['initial_position'] = (float(inputs[0].get()), float(inputs[1].get()), float(inputs[2].get()))
                    save()

            for name, crazyflie in cfg['robots'].items():
                inputs = []
                
                frame = Frame(drone_window)
                frame.pack()

                button = Button(frame, text=name, command=lambda: None)
                button.pack(side=LEFT)

                button = Button(frame, text="X", command=lambda: None)
                button.pack(side=LEFT)

                entry = Entry(frame, background="white")
                entry.pack(side=LEFT)

                inputs.append(entry)

                button = Button(frame, text="Y", command=lambda: None)
                button.pack(side=LEFT)

                entry = Entry(frame, background="white")
                entry.pack(side=LEFT)

                inputs.append(entry)

                button = Button(frame, text="Z", command=lambda: None)
                button.pack(side=LEFT)

                entry = Entry(frame, background="white")
                entry.pack(side=LEFT)

                inputs.append(entry)
                
                submit_button = Button(frame, text="Submit", command=partial(change_cf_position, *(name, crazyflie, inputs)))
                submit_button.pack()

            def confirm():
                top.destroy()
                root.destroy()
                main()
            submit_frame = Frame(drone_window)
            submit_frame.pack()
            submit_button = Button(submit_frame, text="Confirm", command=confirm)
            submit_button.pack()


        def led_color():
            nodes = selected_cfs()
            
            def chooser_color():
                color_code = colorchooser.askcolor(title="Choose color")
                for name, crazyflie in nodes.items():
                    uri = crazyflie["uri"]
                    r = color_code[0][0]
                    g = color_code[0][1]
                    b = color_code[0][2]

                    red, green, blue = r, g, b
                    subprocess.call(["ros2 run crazyflie setParam --uri {} --parameter ring.effect --valUint8 {}".format(uri, 7)], shell=True)
                    time.sleep(0.1)
                    subprocess.call(["ros2 run crazyflie setParam --uri {} --parameter ring.solidRed --valUint8 {}".format(uri, red)], shell=True)
                    subprocess.call(["ros2 run crazyflie setParam --uri {} --parameter ring.solidGreen --valUint8 {}".format(uri, green)], shell=True)
                    subprocess.call(["ros2 run crazyflie setParam --uri {} --parameter ring.solidBlue --valUint8 {}".format(uri, blue)], shell=True)
            # I can not see what is wrong with spaces here
            def chooser_color_by_cf():
                for name, crazyflie in nodes.items():
                    uri = crazyflie["uri"]
                    color_code = colorchooser.askcolor(title="Choose color for {}".format(name))
                    r = color_code[0][0]
                    g = color_code[0][1]
                    b = color_code[0][2]

                    red, green, blue = r, g, b
                    subprocess.call(["ros2 run crazyflie setParam --uri {} --parameter ring.effect --valUint8 {}".format(uri, 7)], shell=True)
                    time.sleep(0.1)
                    subprocess.call(["ros2 run crazyflie setParam --uri {} --parameter ring.solidRed --valUint8 {}".format(uri, red)], shell=True)
                    subprocess.call(["ros2 run crazyflie setParam --uri {} --parameter ring.solidGreen --valUint8 {}".format(uri, green)], shell=True)
                    subprocess.call(["ros2 run crazyflie setParam --uri {} --parameter ring.solidBlue --valUint8 {}".format(uri, blue)], shell=True)

            def stop():
                for name, crazyflie in nodes.items():
                    uri = crazyflie["uri"]
                    red, green, blue = 0, 0, 0
                    subprocess.call(["ros2 run crazyflie setParam --uri {} --parameter ring.effect --valUint8 {}".format(uri, 7)], shell=True)
                    subprocess.call(["ros2 run crazyflie setParam --uri {} --parameter ring.solidRed --valUint8 {}".format(uri, red)], shell=True)
                    subprocess.call(["ros2 run crazyflie setParam --uri {} --parameter ring.solidGreen --valUint8 {}".format(uri, green)], shell=True)
                    subprocess.call(["ros2 run crazyflie setParam --uri {} --parameter ring.solidBlue --valUint8 {}".format(uri, blue)], shell=True)
                    # subprocess.call(["ros2 run crazyflie setParam --uri {} --parameter ring.effect --valUint8 {}".format(uri, 7)], shell=True)
                    # time.sleep(0.1)


            root = Tk()
            root.title("Pick the color combination!")
            button = Button(root, text="Select color", command = chooser_color)
            button_led_off = Button(root, text="LED off", command = stop)
            button_led_for_each_cf = Button(root, text="Choose Color by CF", command = chooser_color_by_cf)

            button.pack()
            button_led_for_each_cf.pack()
            button_led_off.pack()
            root.geometry("300x300")
            root.mainloop()
    
        def reboot():
            nodes = selected_cfs()
            for name, crazyflie in nodes.items():
                uri = crazyflie["uri"]
                print(name)
                subprocess.call(["ros2 run crazyflie reboot --uri " + uri], shell=True)

        def flashSTM():
            nodes = selected_cfs()
            for name, crazyflie in nodes.items():
                uri = crazyflie["uri"]
                print("Flash STM32 FW to {}".format(uri))
                subprocess.call(["ros2 run crazyflie flash --uri " + uri + " --target stm32 --filename " + args.stm32Fw], shell=True)

        def flashNRF():
            nodes = selected_cfs()
            for name, crazyflie in nodes.items():
                uri = crazyflie["uri"]
                print("Flash NRF51 FW to {}".format(uri))
                subprocess.call(["ros2 run crazyflie flash --uri " + uri + " --target nrf51 --filename " + args.nrf51Fw], shell=True)

        def checkBattery():
            # reset color
            for id, w in widgets.items():
                w.batteryLabel.config(foreground='#999999')

            # query each CF
            nodes = selected_cfs()
            for name, crazyflie in nodes.items():
                uri = crazyflie["uri"]
                cfType = crazyflie["type"]
                bigQuad = cfTypes[cfType]["big_quad"]
                
                try:
                    if not bigQuad:
                        voltage = subprocess.check_output(["ros2 run crazyflie battery --uri " + uri], shell=True)
                    else:
                        voltage = subprocess.check_output(["ros2 run crazyflie battery --uri " + uri + " --external 1"], shell=True)
                except subprocess.CalledProcessError:
                    voltage = None  # CF not available

                color = '#000000'
                if voltage is not None:
                    voltage = float(voltage)
                    if voltage < cfTypes[cfType]["battery"]["voltage_warning"]:
                        color = '#FF8800'
                    if voltage < cfTypes[cfType]["battery"]["voltage_critical"]:
                        color = '#FF0000'
                    widgetText = "{:.2f} v".format(voltage)
                else:
                    widgetText = "Err"

                widgets[name].batteryLabel.config(foreground=color, text=widgetText)

        scriptButtons = Tkinter.Frame(top)
        mkbutton(scriptButtons, "battery", checkBattery)
        # currently not supported
        # mkbutton(scriptButtons, "version", checkVersion)
        mkbutton(scriptButtons, "sysOff", sysOff)
        mkbutton(scriptButtons, "reboot", reboot)
        mkbutton(scriptButtons, "positions", change_positions)
        # added mkbutton not sure if it is right
        mkbutton(scriptButtons, "led_color", led_color)

        # mkbutton(scriptButtons, "flash (STM)", flashSTM)
        # mkbutton(scriptButtons, "flash (NRF)", flashNRF)

        # start background threads
        
    def checkBatteryLoop():
            while True:
                # rely on GIL
                checkBattery()
                time.sleep(10.0) # seconds
        # checkBatteryThread = threading.Thread(target=checkBatteryLoop)
        # checkBatteryThread.daemon = True # so it exits when the main thread exit
        # checkBatteryThread.start()

        # place the widgets in the window and start
    buttons.pack()
    frame.pack(padx=10, pady=10)
    scriptButtons.pack()
    top.mainloop()



if __name__ == '__main__':
    main()