import os.path
import sys
import mmap, re
from tkinter import CENTER
import warnings

from datetime import datetime

from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

matplotlib.use("TkAgg")

import PySimpleGUI as sg

from rotation import Rotation
from orientation import Orientation

# from fieldFox import FieldFox
print("imported orientation")

sg.theme("DarkBlue12")


# Creates the main window (type: sg.window)
def make_window():
    filterTip = "Filter files\nType in box to narrow down the list of files.\nFile list will update with list of files with string in filename."
    threshTip = "Enter acceptable threshold\nMay vary depending on satellite"
    aziTip = "Manually input desired azimuth"
    eleTip = "Manually input desired elevation"

    outputs = [
        [sg.Text(key="Az limit switch")],
        [sg.Text(key="Az Angle")],
        [sg.Text(key="El Angle")],
        [sg.Text(key="FF input")],
        [sg.Text(key="Pol value")],
    ]
    outputsFr = sg.Frame("Readings", outputs)

    polarization = [
        [sg.Button("Pol right")],
        [sg.Button("Pol left")],
        [sg.Button("Stop pol", button_color=('green'))],
        [sg.Text("Enter desired pol angle")],
        [
            sg.Input(
                size=(10, 1),
                key="pol_angle",
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
            )
        ],
        [sg.Button("Auto Peak")],
    ]
    autoPeakFr = sg.Frame("Auto Peak", autoPeak)

    orientCal = [
        [sg.Button("Orient Init")],
    ]
    orientCalFr = sg.Frame("Calibrate Orientation", orientCal)

    leftCol = [
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
        [polarizationFr],
    ]

    rightCol = [
        [autoFindFr],
        [orientCalFr],
        [autoPeakFr],
        [sg.Button("Close GUI")],
    ]

    layout = [
        [sg.Text("Manual Antenna Control", font="Any 20")],
        [
            sg.Column(leftCol, element_justification="c"),
            sg.Column(midCol, element_justification="c"),
            sg.Column(rightCol, element_justification="c"),
        ],
    ]

    return layout


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


# Create the Window
window = sg.Window("Manual antenna control", make_window(), finalize=True)


# Instantiate rotate class
myRotate = Rotation(GUI_test=True)
orient = Orientation()
# orient.orientation_init()
# mySignal = FieldFox()

# CONSIDER CREATING A FUNCTION DICT???

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read(timeout=10)
    if (
        event == sg.WIN_CLOSED or event == "Close GUI"
    ):  # if user closes window or clicks Close GUI
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
        # myRotate.autoFindTest()
    elif event == "Orient Init":
        print("Orient Init")
        # orient.orientation_init()
    elif event == "Pol right":
        print("Pol right")
        # myRotate.polRight()
    elif event == "Pol left":
        print("Pol left")
        # myRotate.polLeft()
    elif event == "Stop pol":
        print("Stop pol")
        # myRotate.stopPol()
    elif event == "Auto Pol":
        print("Auto Pol")
        print(values["pol_angle"])
        # myRotate.autoPol(values["pol_angle"])
    elif event == "Auto Peak":
        print("Auto Peak")
        print(f"Freq: {values['autopeak_freq']}")
        # myRotate.autoPeak(values['autopeak_freq'])

    window["Az limit switch"].update(f"Az lim: {myRotate.readLimAz()}")
    window["El Angle"].update(f"El Angle: {myRotate.getElAngle()}")
    window["Az Angle"].update(f"Az Angle: {myRotate.getAzAngle()}")
    window["Pol value"].update(f"Pol value: {myRotate.getPolAngle()}")
    # window["Az ticks"].update(f"Az ticks: {myRotate.getAzTicks()}")
    # window["El ticks"].update(f"El ticks: {myRotate.getElTicks()}")
    # window["FF input"].update(f"Channel power: {mySignal.readSig()}")
