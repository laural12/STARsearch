def ui():
    '''this is the main function that interacts with the user'''
    display()

    #wait for input

    if gui.input == execute:
        #send selections from GUI to toBrain()
        toBrain(gui.command)

    elif gui.input == kill:
        kill()


    while not acquired:
        light(green, flash)
        #show progress indicator
        #perhaps flashing green light

    light(green)
    displayGraphs()

def toBrain(command):
    '''this is the main function that interacts with the brain'''
    send(command.type, command.satellite, command.antenna, command.threshold)

def send(type, satellite=None, antenna=None, threshold=None):
    '''function actually communicates with the brain, only called by toBrain(), uses ethernet'''

def display():
    '''displays GUI to the user, ui() handles all input'''

    if input:
        ui()

def displayGraphs():
    '''shows the informational graphs'''

def kill():
    '''immediately halts all operation'''
    toBrain(command)
    light(red)

def light(color, style=None):
    '''function flashes a light on GUI'''