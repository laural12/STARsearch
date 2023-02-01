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
print("imported orientation")

sg.theme("DarkBlue12")


# Creates the main window (type: sg.window)
def make_window():
    filterTip = "Filter files\nType in box to narrow down the list of files.\nFile list will update with list of files with string in filename."
    threshTip = "Enter acceptable threshold\nMay vary depending on satellite"
    aziTip = "Manually input desired azimuth"
    eleTip = "Manually input desired elevation"

    leftCol = [
        [sg.Text("Azimuth")],
        [sg.Button("Az turn left")],
        [sg.Button("Az turn right")],
        [sg.Button("Reset Az")],
        [sg.Text("Elevation")],
        [sg.Button("El turn left")],
        [sg.Button("El turn right")],
        [sg.Button("Reset El")],
    ]

    midCol = [
        [sg.Text(key="Az limit switch")],
        [sg.Text(key="Az ticks")],
        [sg.Text(key="El ticks")],
    ]

    rightCol = [
        [sg.Text("Pin control")],
        [sg.Button("GPIO 24")],
        [sg.Button("GPIO 21")],
        [sg.Button("GPIO 22")],
        [sg.Button("GPIO 19")],
        [sg.Button("GPIO 28")],
        [sg.Button("GPIO 30")],
        [sg.Button("Reset all")],
        [sg.Button("Cancel")],
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
myRotate = Rotation(GUI_test=False)
orient = Orientation()
orient.orientation_init()

# CONSIDER CREATING A FUNCTION DICT???

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read(timeout=10)
    if (
        event == sg.WIN_CLOSED or event == "Cancel"
    ):  # if user closes window or clicks cancel
        break
    elif event == "Az turn left":
        print("Az turn left")
        myRotate.azTurnLeft()
    elif event == "Az turn right":
        print("Az turn right")
        myRotate.azTurnRight()
    elif event == "El turn left":
        print("El turn left")
        myRotate.elTurnLeft()
    elif event == "El turn right":
        print("El turn right")
        myRotate.elTurnRight()
    elif event == "Reset Az":
        print("Reset Az")
        myRotate.azReset()
    elif event == "Reset El":
        print("Reset El")
        myRotate.elReset()
    elif event == "Reset all":
        print("Reset all")
        myRotate.elReset()
        myRotate.azReset()
    elif event == "GPIO 24":
        print("GPIO 24 to high")
        myRotate.write(24, 1)
    elif event == "GPIO 21":
        print("GPIO 21 to high")
        myRotate.write(21, 1)
    elif event == "GPIO 22":
        print("GPIO 22 to high")
        myRotate.write(22, 1)
    elif event == "GPIO 19":
        print("GPIO 19 to high")
        myRotate.write(19, 1)
    elif event == "GPIO 28":
        print("GPIO 28 to high")
        myRotate.write(28, 1)
    elif event == "GPIO 30":
        print("GPIO 30 to high")
        myRotate.write(30, 1)

    window["Az limit switch"].update(f"Az lim: {myRotate.readLimAz()}")
    window["Az ticks"].update(f"Az ticks: {myRotate.getAzTicks()}")
    window["El ticks"].update(f"El ticks: {myRotate.getElTicks()}")
