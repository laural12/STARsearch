import time
from queue import Queue
import pyvisa
from rotation import Rotation
from orientation import Orientation
import numpy as np


class FieldFox:
    myRotate = Rotation(GUI_test=False)
    orient = Orientation()

    def __init__(self):
        self.ourTime = Queue(maxSize=200)
        self.sigStrength = Queue(maxSize=200)
        self.az = Queue(maxsize=200)
        self.el = Queue(maxsize=200)

        self.powerLevel = 0.0
        self.alpha = 0.9

        self.elWindow = 5.0  # degrees
        self.azWindow = 5.0  # degrees

        self.ip = "10.32.114.148"

        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(f"TCPIP0::{self.ip}::inst0:INSTR")

        # ?

    def readSig(self):
        # return 0
        print(self.inst.query("*IDN?"))

    def sigMakeQsAndLists(self):
        # has a queue of time and signal data
        if self.ourTime.full() != True:
            self.ourTime.put(time.time())
        else:
            self.ourTime.get()
            self.ourTime.put(time.time())

        if self.sigStrength.full() != True:
            self.sigStrength.put(self.readSig())
        else:
            self.sigStrength.get()
            self.sigStrength.put(self.readSig())

        if self.az.full() != True:
            self.az.put(self.myRotate.getAzAngle())
        else:
            self.az.get()
            self.az.put(self.myRotate.getAzAngle())

        if self.el.full() != True:
            self.el.put(self.myRotate.getElAngle())
        else:
            self.el.get()
            self.el.put(self.myRotate.getElAngle())

        timeList = list(self.ourTime.queue)
        sigList = list(self.sigStrength.queue)
        azList = list(self.az.queue)
        elList = list(self.el.queue)

        return timeList, sigList, azList, elList

    def orientPol(self):
        self.oldSig = self.readSig()
        # rotate cw
        newSig = self.readSig()
        if newSig > self.oldSig:
            while newSig > self.oldSig:
                self.oldSig = newSig
                # rotate cw
                newSig = self.readSig()
                return True
        elif newSig < self.oldSig:
            while newSig < self.oldSig:
                self.oldSig = newSig
                # rotate ccw
                newSig = self.readSig()
                return True
        else:
            return True

        return
        # rotate feed to angle of polarization? is this angle known?

    # returns true if the signal has increased, false if not
    def checkIfSigIncrease(self):
        newSig = self.readSig()
        if newSig > self.oldSig:
            self.oldSig = newSig
            return True
        else:
            self.oldSig = newSig
            return False

    def findPeakSig(self):
        # Maximize power over azimuth
        # Might instead want a certain window size - related to time it takes to move x degrees?
        initAz = self.myRotate.getAzAngle()
        self.myRotate.azTurnRight()  # Clockwise is positive

        windSize = 10
        window = np.repeat(0.0, windSize)
        pwrLevels = np.array([])
        azAngles = np.array([])
        while self.myRotate.getAzAngle() < initAz + self.azWindow:
            # Exponential weighted moving average - higher alpha means the average is more resistant to change
            # self.powerLevel = (1 - self.alpha) * self.readSig() + self.alpha * self.powerLevel
            window[:-1] = window[1:]
            window[-1] = self.readSig()

            # Record average power at this level
            pwrLevels = np.append(pwrLevels, np.mean(window))
            azAngles = np.append(
                azAngles, self.myRotate.getAzAngle()
            )  # and record corresponding azimuth angle

        self.myRotate.azTurnLeft()  # CCW is negative
        while self.myRotate.getAzAngle() > initAz - self.azWindow:
            # self.powerLevel = (1 - self.alpha) * self.readSig() + self.alpha * self.powerLevel
            window[:-1] = window[1:]
            window[-1] = self.readSig()

            # Record average power at this level
            pwrLevels = np.append(pwrLevels, np.mean(window))
            azAngles = np.append(
                azAngles, self.myRotate.getAzAngle()
            )  # and record corresponding azimuth angle

        bestAz = azAngles[np.argmax(pwrLevels)]
        self.myRotate.azTurnRight()
        while self.myRotate.getAzAngle() < bestAz:
            time.sleep(0.001)
        self.myRotate.azReset()

        # Now maximize power over elevation
        initEl = self.myRotate.getElAngle()
        self.myRotate.elTurnUp()  # Up is positive

        windSize = 10
        window = np.repeat(0.0, windSize)
        pwrLevels = np.array([])
        elAngles = np.array([])
        while self.myRotate.getElAngle() < initEl + self.elWindow:
            # Exponential weighted moving average - higher alpha means the average is more resistant to change
            # self.powerLevel = (1 - self.alpha) * self.readSig() + self.alpha * self.powerLevel
            window[:-1] = window[1:]
            window[-1] = self.readSig()

            # Record average power at this level
            pwrLevels = np.append(pwrLevels, np.mean(window))
            elAngles = np.append(
                elAngles, self.myRotate.getElAngle()
            )  # and record corresponding azimuth angle

        self.myRotate.elTurnDown()  # Down is negative
        while self.myRotate.getElAngle() > initAz - self.azWindow:
            # self.powerLevel = (1 - self.alpha) * self.readSig() + self.alpha * self.powerLevel
            window[:-1] = window[1:]
            window[-1] = self.readSig()

            # Record average power at this level
            pwrLevels = np.append(pwrLevels, np.mean(window))
            elAngles = np.append(
                elAngles, self.myRotate.getElAngle()
            )  # and record corresponding azimuth angle

        bestEl = elAngles[np.argmax(pwrLevels)]
        self.myRotate.elTurnUp()
        while self.myRotate.getElAngle() < bestEl:
            time.sleep(0.001)
        self.myRotate.elReset()

    def maintainPeakSig(self):
        return
        # if gain decreases, rerun findPeakPol
