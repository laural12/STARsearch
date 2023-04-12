import os.path
import sys
import mmap, re
from tkinter import CENTER
import warnings
import pickle
import time
import threading

from datetime import datetime

from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib

matplotlib.use("TkAgg")

from rotation import Rotation
from orientation import Orientation

print("Launching GUI...")

sg.theme("DarkBlue12")  # Sets the color theme of GUI


# Creates the main window (type: sg.window)
def make_window():
    # Tips are text that appears when you hover over a box
    polTip = "Input desired polarization\n0 or 180: Horizontal\n90: Vertical"
    freqTip = "Enter frequency at which to read power"

    # Put all the options in their own little frames (gives them a border and title)
    outputs = [
        [sg.Text(key="Az limit switch")],
        [sg.Text(key="El limit switch")],
        [sg.Text(key="Az Angle")],
        [sg.Text(key="El Angle")],
        [sg.Text(key="FF input")],
        [sg.Text(key="Pol value")],
    ]
    outputsFr = sg.Frame("Readings", outputs)

    polarization = [
        [sg.Button("Pol right")],
        [sg.Button("Pol left")],
        [sg.Button("Stop pol", button_color=("green"))],
        [sg.Text("Enter desired pol angle")],
        [
            sg.Input(
                size=(10, 1),
                key="pol_angle",
                tooltip=polTip,
            )
        ],
        [sg.Button("Auto Pol")],
    ]
    polarizationFr = sg.Frame("Polarization", polarization)

    autoFind = [
        [sg.Text("Enter desired azimuth")],
        [
            sg.Input(
                size=(10, 1),
                key="autofind_az",
            )
        ],
        [sg.Text("Enter desired elevation")],
        [
            sg.Input(
                size=(10, 1),
                key="autofind_el",
            )
        ],
        [sg.Button("Auto Find")],
    ]
    autoFindFr = sg.Frame("Auto Find", autoFind)

    autoPeak = [
        [sg.Text("Enter frequency")],
        [
            sg.Input(
                size=(10, 1),
                key="autopeak_freq",
                tooltip=freqTip,
            )
        ],
        [sg.Button("Auto Peak")],
    ]
    autoPeakFr = sg.Frame("Auto Peak", autoPeak)

    orientCal = [
        [sg.Button("Orient Init")],
    ]
    orientCalFr = sg.Frame("Calibrate Orientation", orientCal)

    presets = [
        [sg.Text("Choose Satellite:")],
        [sg.Combo(["Galaxy 16", "SES 1"], key="sat")],
        [sg.Button("Acquire")],
    ]
    presetsFr = sg.Frame("Presets", presets)

    # Organize the GUI elements into columns
    leftCol = [
        [sg.Text("Choose Antenna:")],
        [sg.Combo(["Antenna 1", "Antenna 2", "Antenna 3"], key="ant")],
        [sg.Text("Azimuth")],
        [sg.Button("Az turn left")],
        [sg.Button("Az turn right")],
        [sg.Button("Stop Az", button_color=("green"))],
        [sg.Text("Elevation")],
        [sg.Button("El turn down")],
        [sg.Button("El turn up")],
        [sg.Button("Stop El", button_color=("green"))],
        [sg.Text("Stop all")],
        [sg.Button("Stop all", button_color=("green"))],
    ]

    midCol = [
        [outputsFr],
        [presetsFr],
        [polarizationFr],
    ]

    rightCol = [
        [autoFindFr],
        [orientCalFr],
        [autoPeakFr],
        [sg.Button("Close GUI")],
    ]

    # Specify the layout
    layout = [
        [sg.Text("STAR Control", font="Any 20")],
        [
            sg.Column(leftCol, element_justification="c"),
            sg.Column(midCol, element_justification="c"),
            sg.Column(rightCol, element_justification="c"),
        ],
    ]

    return layout


# Needed for drawing matplotlib figures (which we don't do, but the capability is here)
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


# Also needed for drawing matplotlib figures
def fig_maker():
    plt.clf()
    plt.close()
    plt.figure(figsize=(3, 3))
    plt.scatter(np.random.rand(1, 10), np.random.rand(1, 10))
    plt.title("Signal Strength over Time")
    plt.ylabel("Signal Strength")
    plt.xlabel("Time")

    return plt.gcf()


# Create the Window
window = sg.Window("STAR Control", make_window(), finalize=True)


# Instantiate rotate class
myRotate = Rotation(GUI_test=False)

# So it doesn't weirdly start moving everything
myRotate.elReset()
myRotate.azReset()
myRotate.polReset()

threadList = list()

# Dictionary of satellite info
galaxy16 = {"az": 150.0, "el": 42.5, "pol": 0.0}
ses1 = {"az": 153.0, "el": 42.2, "pol": 90.0}
satInfo = {"Galaxy 16": galaxy16, "SES 1": ses1}

fig_agg = None
while True:
    event, values = window.read(timeout=10)
    if (
        event == sg.WIN_CLOSED or event == "Close GUI"
    ):  # if user closes window or clicks Close GUI
        currOrient = {"az": myRotate.getAzAngle(), "el": myRotate.getElAngle()}
        with open("currOrient.pickle", "wb") as handle:
            pickle.dump(currOrient, handle, protocol=pickle.HIGHEST_PROTOCOL)
        break
    elif event == "Az turn left":
        print("Az turn left")
        myRotate.azTurnLeft()
    elif event == "Az turn right":
        print("Az turn right")
        myRotate.azTurnRight()
    elif event == "El turn down":
        print("El turn down")
        myRotate.elTurnDown()
    elif event == "El turn up":
        print("El turn up")
        myRotate.elTurnUp()
    elif event == "Stop Az":
        print("Stop Az")
        myRotate.azReset()
    elif event == "Stop El":
        print("Stop El")
        myRotate.elReset()
    elif event == "Stop all":
        print("Stop all")
        myRotate.elReset()
        myRotate.azReset()
    elif event == "Auto Find":
        print("Auto Find")
        print(f"az: {values['autofind_az']}")
        print(f"el: {values['autofind_el']}")
        try:
            # myRotate.autoFind(
            #     float(values["autofind_az"]), float(values["autofind_el"])
            # )
            desAz = float(values["autofind_az"])
            desEl = float(values["autofind_el"])
            x = threading.Thread(
                target=myRotate.autoFind,
                args=(desAz, desEl),
                daemon=True,  # Might want to set it false if you want this thread to finish
            )
            threadList.append(x)
            x.start()
        except ValueError:
            print("Bad input: please enter a number")
    elif event == "Orient Init":
        print("Orient Init")
        # myRotate.initialize_orientation()
        x = threading.Thread(
            target=myRotate.initialize_orientation,
            args=(),
            daemon=True,  # Might want to set it false if you want this thread to finish
        )
        threadList.append(x)
        print("here 1")
        x.start()
        print("here 2")
    elif event == "Pol right":
        print("Pol right")
        myRotate.polTurnRight()
    elif event == "Pol left":
        print("Pol left")
        myRotate.polTurnLeft()
    elif event == "Stop pol":
        print("Stop pol")
        myRotate.polReset()
        # threadList = list()
        # x = threading.Thread(
        #     target=threadFunc,
        #     args=(),
        #     daemon=True,  # Might want to set it false if you want this thread to finish
        # )
        # threadList.append(x)
        # x.start()
        # threadFunc()
    elif event == "Auto Pol":
        print("Auto Pol")
        print(values["pol_angle"])

        try:
            desPol = [float(values["pol_angle"])]
            x = threading.Thread(
                target=myRotate.autoPol,
                args=(desPol),
                daemon=True,  # Might want to set it false if you want this thread to finish
            )
            threadList.append(x)
            x.start()
        except ValueError:
            print("Bad input: please enter a number")
    elif event == "Auto Peak":
        print("Auto Peak")
        print(f"Freq: {values['autopeak_freq']}")
        # myRotate.autoPeak(values["autopeak_freq"])
        x = threading.Thread(
            target=myRotate.autoPeak,
            args=([values["autopeak_freq"]]),
            daemon=True,  # Might want to set it false if you want this thread to finish
        )
        threadList.append(x)
        x.start()
    elif event == "Acquire":
        print("Acquire")
        print(f"Antenna: {values['ant']}")
        print(f"Satellite: {values['sat']}")
        # myRotate.autoFind(satInfo[values["sat"]]["az"], satInfo[values["sat"]]["el"])
        # myRotate.autoPol(satInfo[values["sat"]]["pol"])
        x = threading.Thread(
            target=myRotate.autoFind,
            args=(satInfo[values["sat"]]["az"], satInfo[values["sat"]]["el"]),
            daemon=True,  # Might want to set it false if you want this thread to finish
        )
        threadList.append(x)
        x.start()

        x = threading.Thread(
            target=myRotate.autoPol,
            args=(satInfo[values["sat"]]["pol"]),
            daemon=True,  # Might want to set it false if you want this thread to finish
        )
        threadList.append(x)
        x.start()

    window["Az limit switch"].update(f"Az lim: {myRotate.readLimAz()}")
    window["El limit switch"].update(f"El lim: {myRotate.readLimEl()}")
    # window["El Angle"].update(f"El Angle: {myRotate.getElAngle()}")
    window["El Angle"].update("El Angle: %.5f" % myRotate.getElAngle())
    # window["Az Angle"].update(f"Az Angle: {myRotate.getAzAngle()}")
    window["Az Angle"].update("Az Angle: %.5f" % myRotate.getAzAngle())
    # window["Pol value"].update(f"Pol value: {myRotate.getPolAngle()}")
    window["Pol value"].update("Pol Angle: %.5f" % myRotate.getPolAngleDisp())
    # window["Az ticks"].update(f"Az ticks: {myRotate.getAzTicks()}")
    # window["El ticks"].update(f"El ticks: {myRotate.getElTicks()}")
    # window["FF input"].update(f"Channel power: {myRotate.getChPower()}")
    window["FF input"].update("Channel power: %.5f" % 0.0)
