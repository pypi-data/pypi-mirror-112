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
import queue
import threading
import re
import time
import requests
from pint import UnitRegistry

TIME_OUT = 3
ureg = UnitRegistry()
MOTOR_SPREADER = 2
MOTOR_CRAB = 1
MOTOR_CHASSIS = 3
MOTOR_DIRECTION_BACKWARD = -1
MOTOR_DIRECTION_FORWARD  = 1




class Crane():
    """ This class is used to control cranes"""
    def __init__(self):
        """
        Creates the crane object. each crane has 3 motors, each with a Thread and a queue

        Returns
        -------
        None.
        """
        self.slave_ip = None
        self.master_ip = None
        self.dict_q = {}
        for i in range(1,4):
            self.dict_q[i] = queue.Queue()
            threading.Thread(target = self.run_start_for, daemon = True, args=(i,)).start()


    def run_start_for(self, id_moteur):
        """
        Parameters
        ----------
        id_moteur : int
            DESCRIPTION: It is the motor number

        Raises
        ------
        RuntimeError
            DESCRIPTION Return a RuntimeError when the number
            of motor is different from 1, 2 or 3

        Returns
        -------
        None.
        """
        if id_moteur not in self.dict_q.keys() :
            raise RuntimeError("motor_id Error")
        while True:
            arguments = self.dict_q[id_moteur].get()
            init_time = time.time()*ureg.second
            while time.time()*ureg.second - init_time < arguments[0]:
                self.start(arguments[1], arguments[2])
                if not self.dict_q[id_moteur].empty():
                     break
            self.stop(arguments[1])
            self.dict_q[id_moteur].task_done()



    def get_motor_info_from_number(self, snr):
        """
        Parameters
        ----------
        snr : int
            DESCRIPTION : It is the motornumber

        Raises
        ------
        TypeError
            DESCRIPTION : This exception is raised when the snr parameter is not an integer
        RuntimeError
            DESCRIPTION: This exception is raised when the motor number passed in parameter
                        is different from 1, 2 and 3

        Returns
        -------
        TYPE
            DESCRIPTION.
        int
            DESCRIPTION.
        """
        if not isinstance(snr, int):
            raise TypeError(" The value of n must be an integer but got " +str(snr))



        if MOTOR_SPREADER == snr:
            return (self.slave_ip, 2)
        if MOTOR_CRAB == snr:
            return (self.slave_ip, 1)
        if MOTOR_CHASSIS  == snr:
            return (self.master_ip, 1)
        raise RuntimeError("""Invalid motor number, must be MOTOR_SPREADER, MOTOR_CRAB or
                               MOTOR_CHASSIS , got """+str(snr))


    def start (self, snr, turn):
        """
        Parameters
        ----------
        snr : int
            DESCRIPTION : It is the motor number
        turn : int
            DESCRIPTION : Direction in which we want the motor to go (-1 or 1)
                          MOTOR_DIRECTION_BACKWARD = -1
                          MOTOR_DIRECTION_FORWARD  = 1

        Returns
        -------
        TYPE : string
            DESCRIPTION : Return 'ok' when everything went well

        """

        if turn not in [MOTOR_DIRECTION_FORWARD , MOTOR_DIRECTION_BACKWARD ]:
            raise RuntimeError("""Invalid parameter, turn must be either MOTOR_DIRECTION_FORWARD  or
                                  MOTOR_DIRECTION_BACKWARD . Got """ +str(turn))

        i_p, num_motor = self.get_motor_info_from_number(snr)
        request_answer = requests.get("http://"+i_p+"/startM?sNr="+str(num_motor)+
                                      "&turn="+str(turn), timeout=TIME_OUT)

        if request_answer.status_code !=200:
            raise RuntimeError("Unable to control the motor, "+str(request_answer.status_code))

        if request_answer.text != "ok":
            raise RuntimeError("""Able to controle the motor but got not OK
                                   answer: """+request_answer.text)
        return request_answer.text

    def stop(self, snr):
        """
        Parameters
        ----------
        snr : int
            DESCRIPTION : It is the motor number

        Returns
        -------
        TYPE : string
            DESCRIPTION : Return 'ok' when everything went well
        """

        i_p, num_motor = self.get_motor_info_from_number(snr)
        request_answer = requests.get("http://"+i_p+"/stopM?sNr="+str(num_motor), timeout=TIME_OUT)
        if request_answer.status_code !=200:
            raise RuntimeError("Unable to control the motor, "+str(request_answer.status_code))

        if request_answer.text != "ok":
            raise RuntimeError("""Able to controle the motor but got not OK answer: """+
                               request_answer.text)
        return request_answer.text


    def step (self, snr, turn):
        """
        Parameters
        ----------
        snr : int
            DESCRIPTION : It is the motor number
        turn : int
            DESCRIPTION : Direction in which we want the motor to go (-1 or 1)
                          MOTOR_DIRECTION_BACKWARD = -1
                          MOTOR_DIRECTION_FORWARD  = 1

        Returns
        -------
        TYPE : tuple of string
            DESCRIPTION : Returns the result of the execution of the start and stop functions

        """
        return (self.start(snr, turn), self.stop(snr))


    def start_for(self, time_, snr, turn ):
        """
        Parameters
        ----------
        time_ : float or int
            DESCRIPTION : Represents the time during which we would like to run the motor
        snr : int
            DESCRIPTION : It is the motor number
        turn : int
            DESCRIPTION : Direction in which we want the motor to go (-1 or 1)
                          MOTOR_DIRECTION_BACKWARD = -1
                          MOTOR_DIRECTION_FORWARD  = 1

        Returns
        -------
        None.

        Example
        -------
        start_for(5000*ureg.nanosecond,MOTOR_CHASSIS ,MOTOR_DIRECTION_FORWARD )
        """

        if snr not in [MOTOR_CHASSIS , MOTOR_SPREADER, MOTOR_CRAB]:
            raise RuntimeError("""Invalid parameter, sNr must be either MOTOR_CHASSIS  or
                                MOTOR_SPREADER or MOTOR_CRAB . Got """ +str(snr))

        if time_ < 0:
            raise ValueError("t must be greater than 0 but got "+str(time_))

        arguments = [time_, snr, turn]
        self.dict_q[snr].put(arguments)

    def fswitch(self, value):
        """
        Parameters
        ----------
        value : int
            DESCRIPTION.

        Returns
        -------
        TYPE : string
            DESCRIPTION : eturn 'ok' when everything went well

        """
        request_answer=requests.get("http://"+self.slave_ip+"/fswitch?nr=3"+"&v="+str(value)+
                                    "&dim=1", timeout=TIME_OUT)
        return request_answer.text

    def _get_battery(self):
        """
        Returns
        -------
        TYPE int
            DESCRIPTION it is the state of the baterries
        """
        answer_1 = requests.get("http://"+self.master_ip+"/getBat?n=1", timeout=TIME_OUT)
        answer_2 = requests.get("http://"+self.slave_ip+"/getBat?n=2", timeout=TIME_OUT)

        if answer_1.status_code != 200:
            raise RuntimeError("Please check if the battery  1 is correctly powered")

        if answer_2.status_code != 200:
            raise RuntimeError("Please check if the battery 2 is correctly powered")

        return (int(answer_1.text), int(answer_2.text))

    battery = property(_get_battery)

    def change_speed(self, snr, diff):
        """
        Parameters
        ----------
        snr : int
            DESCRIPTION : it is the motor number
        diff : int
            DESCRIPTION : It is used to vary the speed of the motor

        Returns
        -------
        num : int
            DESCRIPTION : returns the value of the current speed of the motor

        """
        if not isinstance (diff, int):
            raise TypeError("diff must be an int but got "+str(diff))

        i_p, num_motor = self.get_motor_info_from_number(snr)
        request_answer = requests.get("http://"+i_p+"/changePWMTV?sNr="+str(num_motor)+"&diff="+
                                      str(diff), timeout=TIME_OUT)

        if request_answer.status_code != 200:
            raise RuntimeError(""""Unable to change the speed of the motor,"""+
                                str(request_answer.status_code))

        result = re.search("neuer Speed=\s+(\d+)", request_answer.text)
        num = int(result.groups()[0])
        return num

    def get_speed(self , snr):
        """
        Parameters
        ----------
        snr : TYPE
            DESCRIPTION :  is the motor number

        Returns
        -------
        TYPE : int
            DESCRIPTION : Returns the current speed for a motor

        """

        return self.change_speed(snr, 0)

    def set_speed(self , snr, speed):
        """
        Parameters
        ----------
        snr : int
            DESCRIPTION : is the motor number
        speed : int
            DESCRIPTION : set the speed for a motor

        Returns
        -------
        TYPE : int
            DESCRIPTION : returns the value of the current speed of the motor

        """
        current = self.change_speed(snr, 0)
        diff = speed - current
        return self.change_speed(snr, diff)

    def init (self, i_p):
        """
        Parameters
        ----------
        i_p : string
            DESCRIPTION :
        The purpose of this function is to initialize the IP address of
        the master and once the IP address of the master is
        initialized to obtain that of the slave thanks to the getOtherEsp function

        Returns
        -------
        None.

        """

        self.master_ip = i_p
        self.slave_ip = self.get_other_esp(i_p)

    def get_other_esp(self, i_p):
        """
        Parameters
        ----------
        i_p : string
            DESCRIPTION :  This function has the role of launching a request
                            to obtain the IP address of the slave

        Returns
        -------
        TYPE : string
            DESCRIPTION : Return 'ok' when everything went well

        """
        request_answer = requests.get("http://" + i_p + "/getOtherEsp", timeout = TIME_OUT)
        if request_answer.status_code != 200:
            raise RuntimeError ("""I failed to get the IP address of the slave.
            Check if the latter is correctly supplied then try again""")
        return request_answer.text



if __name__ == "__main__":


    i_p1 = "172.17.217.217"
    i_p2 = "172.17.217.217"

    crane_1 = Crane()
    crane_2 = Crane()

    crane_1.init(i_p1)
    crane_2.init(i_p1)


    crane_1.start_for(0.01*ureg.second, MOTOR_SPREADER, MOTOR_DIRECTION_BACKWARD )
    crane_2.start_for(0.01*ureg.second, MOTOR_CRAB, MOTOR_DIRECTION_FORWARD )

    crane_1.start_for(0.092*ureg.second, MOTOR_CRAB, MOTOR_DIRECTION_FORWARD )
    print(crane_1.fswitch(0))
    print(crane_1.battery)
    print(crane_1.change_speed(MOTOR_CRAB, -40))
    crane_2.start_for(0.01*ureg.second, MOTOR_CHASSIS , MOTOR_DIRECTION_FORWARD )

    print(crane_2.change_speed(MOTOR_SPREADER,20))
    print(crane_2.battery)
    crane_2.step(MOTOR_CHASSIS  ,MOTOR_DIRECTION_BACKWARD )
    crane_1.step(MOTOR_CRAB, MOTOR_DIRECTION_BACKWARD )
    print (crane_1.get_speed(MOTOR_CRAB))

