"""
    Created on Tue May 4 2021
"""
# -*-coding: <Utf-8> -*-
# -*-coding: <Utf-8> -*-
from dccpi import *

e = DCCRPiEncoder()
controller = DCCController(e) #Create the DCC controller with the RPi encoder

def start():
    """ Starts the controller and Removes a brake signal """
    controller.start()
def stop():
    """ This function stops the controller and enables a brake signal on tracks"""
    controller.stop()



class DCCObject(object):
    """ Speedlib librairie to control a locomive device"""
    def __init__(self, name, adress):
        """ this function takes a name and an address (an integer # 0) as
        parameters to create a train and  register it  on the controller
        """
        self.name = name
        self.adress = adress
        self._l = DCCLocomotive(name, adress)  # Create locos, args: Name, DCC Address
        controller.register(self._l)  # Register locos on the controller
        self.speed = 0
        self.fl = False
        self.f1 = False
        self.f2 = False
        self.f3 = False
        self.f4 = False

    def reverse(self):
        """Change the direction"""
        self._l.reverse()

    def faster(self):
        """ Increase 1 speed step"""
        self._l.faster()

    def slower(self):
        """Reduce the speed"""
        self._l.slower()

    def _get_speed(self):
        """ Returns the current speed of the train """
        return self._l.speed

    def _set_speed(self, new_speed):
        """ change the speed"""
        if not isinstance(new_speed, int):
            raise TypeError("vew_speed must be an integer but get "+ str(new_speed))
        self._l.speed = new_speed
    speed = property(_get_speed, _set_speed)

    def __repr__(self):
        return """ DCC locomotive : Name = {},
        address = {},
        speed = {}, 
        fl = {}, 
        f1 = {}, 
        f2 = {},
        f3 = {}, 
        f4 = {} """.format(self.name, self.adress,
                           self._l.speed, self._l.fl,
                           self._l.f1, self._l.f2,
                           self._l.f3, self._l.f4)


    def _get_f_light(self):
        """Returns the current state of fl """
        return self._l.fl

    def _set_f_light(self, var):
        """ change the state of fl """
        if not isinstance(var, bool):
            raise TypeError("var must be a bool but got "+str(var))
        self._l.fl = var
    f_light = property(_get_f_light, _set_f_light)

    def _get_f1(self):
        """Returns the current state of f1 """
        return self._l.f1

    def _set_f1(self, var):
        """ change the state of f1 """
        if not isinstance(var, bool):
            raise TypeError("var must be a bool but got "+str(var))
        self._l.f1 = var
    f1 = property(_get_f1, _set_f1)

    def _get_f2(self):
        """Returns the current state of f2 """
        return self._l.f2

    def _set_f2(self, var):
        """ change the state of f2 """
        if not isinstance(var, bool):
            raise TypeError("var must be a bool but got "+str(var))
        self._l.f2 = var
    f2 = property(_get_f2, _set_f2)

    def _get_f3(self):
        """Returns the current state of f3 """
        return self._l.f3

    def _set_f3(self, var):
        """ change the state of f3 """
        if not isinstance(var, bool):
            raise TypeError("var must be a bool but got "+str(var))
        self._l.f3 = var
    f3 = property(_get_f3, _set_f3)

    def _get_f4(self):
        """Returns the current state of f4 """
        return self._l.f4

    def _set_f4(self, var):
        """ change the state of fl """
        if not isinstance(var, bool):
            raise TypeError("var must be a bool but got "+str(var))
        self._l.f4 = var
    f4 = property(_get_f4, _set_f4)
