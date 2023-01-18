import os.path
import sys
import mmap, re
from tkinter import CENTER
import warnings

from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

matplotlib.use("TkAgg")

import PySimpleGUI as sg

from rotateTest import Rotation

sg.theme("DarkBlue12")


# Creates the main window (type: sg.window)
def make_window():
    filterTip = "Filter files\nType in box to narrow down the list of files.\nFile list will update with list of files with string in filename."
    threshTip = "Enter acceptable threshold\nMay vary depending on satellite"
    aziTip = "Manually input desired azimuth"
    eleTip = "Manually input desired elevation"

    leftCol = [
        [sg.Button("Az left enable")],
        [sg.Button("El left enable")],
    ]

    midCol = [
        [sg.Button("Az right enable")],
        [sg.Button("El right enable")],
    ]

    rightCol = [
        [sg.Button("Start Az")],
        [sg.Button("Stop Az")],
        [sg.Button("Start El")],
        [sg.Button("Stop El")],
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
myRotate = Rotation()

# CONSIDER CREATING A FUNCTION DICT???

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if (
        event == sg.WIN_CLOSED or event == "Cancel"
    ):  # if user closes window or clicks cancel
        break
    elif event == "Az left enable":
        print("Az left enable")
        myRotate.azLeftEn()
    elif event == "Az right enable":
        print("Az right enable")
        myRotate.azRightEn()
    elif event == "El left enable":
        print("El left enable")
        myRotate.elLeftEn()
    elif event == "El right enable":
        print("El right enable")
        myRotate.elRightEn()
    elif event == "Start Az":
        print("Start Az")
        myRotate.azStart()
    elif event == "Stop Az":
        print("Stop Az")
        myRotate.azStop()
    elif event == "Start El":
        print("Start El")
        myRotate.elStart()
    elif event == "Stop El":
        print("Stop El")
        myRotate.elStop()
