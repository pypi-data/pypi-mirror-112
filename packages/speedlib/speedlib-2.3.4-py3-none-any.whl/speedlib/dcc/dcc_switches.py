"""
    Copyright (C) 2021  CNRS
    This file is part of "Speedlib".
    "Speedlib" is an API built for the use case of autonomous navigation.
    It has  been developed to control quay cranes and trains of multimodal
    waterborne Lab as part of The SPEED project, a project which aims to
    enhance and support the growth of a system of connected port solutions,
    with the use of data science and IoT (Internet of Things) technologies.
    The library allows controlling the motion of the IoT devices at H0 scale
    in automatic mode, in three directions and exchanging with the information
    system for overall management
"""
# -*-coding: <Utf-8> -*-
import dcc_object
from dcc_object import DCCObject
import time
class Switch():
    """ This class is used to control Servo motors """
    def __init__(self, name, adress, biais_id):
        """
        Parameters
        ----------
        name : string
            DESCRIPTION : It is the name of the train
        adress : int
            DESCRIPTION This is the address on which it was programmed
        biais_id : int
            DESCRIPTION Allows you to choose which servomotor will be used
        Returns
        -------
        None.

        """
        self.name = name
        self.adress = adress
        self.biais_id = biais_id

        if not isinstance(self.biais_id, int):
            raise TypeError("biais_id must be an int but got "+str(self.biais_id))
        if self.biais_id not in [1, 2]:
            raise ValueError("biais_id must be an 1 or 2 but got "+str(self.biais_id))
        if not isinstance(name, str):
            raise TypeError(" name must be a str but got " +str(name))
        if not isinstance(adress, int):
            raise TypeError("adress must be an integer but got  " +str(adress))
        #if adress not in range(101, 126):
            #raise RuntimeError("""The address must be between 101 and 125 but got """+str(adress))

        self.dccobject = DCCObject(name, adress)


    def _get_biais(self):
        """
        Returns
        -------
        TYPE
            DESCRIPTION : Returns the current state of the switch

        """
        return self.dccobject.f1, self.dccobject.fl

    def _set_biais(self, state):
        """
        Parameters
        ----------
        var : Boolean
            DESCRIPTION : change the state of the switch

        Returns
        -------
        None.

        """
        if not isinstance(state, bool):
            raise TypeError(" var must me a boolean but got "+str(state))

        if self.biais_id == 1:
            self.dccobject.f1 = state
            self.dccobject.f_light = state

        elif self.biais_id == 2:
            self.dccobject.f2 = state
            self.dccobject.reverse()


    biais = property(_get_biais, _set_biais)



if __name__ == "__main__":
    S = Switch("DCC3", 3, 2)
    dcc_object.start()
    S.biais = False
    time.sleep(3)
    dcc_object.stop()
