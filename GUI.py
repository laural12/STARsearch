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

# Returns Dictionary of files (type: Dict[str:str])
def get_file_list_dict(subFolder):
    demo_path = get_demo_path(subFolder)
    demo_files_dict = {}
    for dirname, dirnames, filenames in os.walk(demo_path):
        for filename in filenames:
            fname_full = os.path.join(dirname, filename)
            if filename not in demo_files_dict.keys():
                demo_files_dict[filename] = fname_full
            else:
                # Allow up to 100 dupicated names. After that, give up
                for i in range(1, 100):
                    new_filename = f"{filename}_{i}"
                    if new_filename not in demo_files_dict:
                        demo_files_dict[new_filename] = fname_full
                        break
    return demo_files_dict


# Returns list of filenames (type: List[str])
def get_file_list(subfolder):
    return sorted(list(get_file_list_dict(subfolder).keys()))


# Returns top-level folder path (type: str)
def get_demo_path(subfolder):
    demo_path = sg.user_settings_get_entry("-demos folder-", os.path.dirname(__file__))
    return demo_path + "/" + subfolder


### UNFINISHED
# Gets signal strength data (type: [int])
def get_sig_str():
    signal = [0, 2, 4, 6, 8, 10]
    return signal


### UNFINISHED
# Gets antenna azimuth data (type: [int])
def get_az():
    azimuth = [1, 2, 3, 4, 5, 6]
    return azimuth


### UNFINISHED
# Gets antenna elevation data (type: [int])
def get_el():
    elevation = [1, 2, 3, 4, 5, 6]
    return elevation


### UNFINISHED
# Gets antenna elevation data (type: [int])
def get_time():
    time = [1, 2, 3, 4, 5, 6]
    return time


# Creates the main window (type: sg.window)
def make_window():
    filterTip = "Filter files\nType in box to narrow down the list of files.\nFile list will update with list of files with string in filename."
    threshTip = "Enter acceptable threshold\nMay vary depending on satellite"
    aziTip = "Manually input desired azimuth"
    eleTip = "Manually input desired elevation"

    leftCol = [
        [
            sg.Listbox(
                values=get_file_list("Antennas"),
                select_mode=sg.SELECT_MODE_EXTENDED,
                size=(45, 10),
                bind_return_key=True,
                key="-DEMO LIST-",
            )
        ],
        [
            sg.Text("Antenna Filter:", tooltip=filterTip),
            sg.Input(
                size=(33, 1),
                focus=True,
                enable_events=True,
                key="-FILTERA-",
                tooltip=filterTip,
            ),
        ],
        [sg.Button("Select")],
        [
            sg.Listbox(
                values=get_file_list("Satellites"),
                select_mode=sg.SELECT_MODE_EXTENDED,
                size=(45, 10),
                bind_return_key=True,
                key="-DEMO LIST-",
            )
        ],
        [
            sg.Text("Satellite Filter:", tooltip=filterTip),
            sg.Input(
                size=(33, 1),
                focus=True,
                enable_events=True,
                key="-FILTERS-",
                tooltip=filterTip,
            ),
        ],
        [sg.Button("Select")],
        [sg.Canvas(key="-CANVAS-")],
    ]

    midCol = [
        [sg.Text("Choose Antenna:")],
        [sg.Combo(["Antenna 1", "Antenna 2", "Antenna 3"], key="Ant")],
        [sg.Text("Choose Acceptable Threshold:")],
        [
            sg.Input(
                size=(33, 1),
                focus=True,
                enable_events=True,
                key="-FILTERTH-",
                tooltip=threshTip,
            )
        ],
        [sg.Button("Continue")],
        [sg.Canvas(key="-CANVAS2-")],
    ]

    rightCol = [
        [sg.Text("Choose Antenna:")],
        [sg.Combo(["Antenna 1", "Antenna 2", "Antenna 3"], key="Ant")],
        [sg.Text("Choose Azimuth:")],
        [
            sg.Input(
                size=(33, 1),
                focus=True,
                enable_events=True,
                key="-FILTERAZ-",
                tooltip=aziTip,
            )
        ],
        [sg.Text("Choose Elevation:")],
        [
            sg.Input(
                size=(33, 1),
                focus=True,
                enable_events=True,
                key="-FILTEREL-",
                tooltip=eleTip,
            )
        ],
        [sg.Button("Continue 2")],
        [sg.Canvas(key="-CANVAS3-")],
        [sg.Button("Cancel")],
    ]

    layout = [
        [sg.Text("antenna control e", font="Any 20")],
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


strData = get_sig_str()
azData = get_az()
elData = get_el()
timeData = get_time()

fig = matplotlib.figure.Figure(figsize=(4, 3.8), dpi=100)
tstr = fig.add_subplot(111)
tstr.set_title("Signal Strength over Time")
tstr.set_ylabel("Signal Strength")
tstr.set_xlabel("Time")
tstr.plot(timeData, strData)


fig2 = matplotlib.figure.Figure(figsize=(4, 3.8), dpi=100)
azstr = fig2.add_subplot(111)
azstr.set_title("Signal Strength vs Azimuth")
azstr.set_ylabel("Signal Strength")
azstr.set_xlabel("Azimuth")
azstr.plot(azData, strData)

fig3 = matplotlib.figure.Figure(figsize=(4, 3.8), dpi=100)
elstr = fig3.add_subplot(111)
elstr.set_title("Signal Strength vs Elevation")
elstr.set_ylabel("Signal Strength")
elstr.set_xlabel("Elevation")
elstr.plot(elData, strData)

# Create the Window
window = sg.Window("Does a thing", make_window(), finalize=True)

strTime = draw_figure(window["-CANVAS-"].TKCanvas, fig)
strTime = draw_figure(window["-CANVAS2-"].TKCanvas, fig2)
strTime = draw_figure(window["-CANVAS3-"].TKCanvas, fig3)

# Instantiate rotate class
myRotate = Rotation()

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if (
        event == sg.WIN_CLOSED or event == "Cancel"
    ):  # if user closes window or clicks cancel
        break
    elif event == "Continue 2":
        myRotate.rotate()
