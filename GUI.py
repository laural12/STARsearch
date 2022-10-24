import PySimpleGUI as sg

sg.theme('DarkBlue1')

layout = [  [sg.Image(filename="STARsearch.png", size=(300,130))],
            [sg.Text('Choose Antenna:')],
            [sg.Combo(['Antenna 1', 'Antenna 2', 'Antenna 3'], background_color='Slategray2', key='Ant', text_color='black')],
            [sg.Text('Choose Satellite:')],
            [sg.Combo(['Satellite 1', 'Satellite 2', 'Satellite 3'], background_color="Slategray2", key='Sat', text_color='black')],
            [sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Antenna Control', layout)


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
