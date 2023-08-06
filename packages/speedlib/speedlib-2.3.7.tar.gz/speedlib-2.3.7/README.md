Tutorial
========

Using the SpeedLib librairie
----------------------------
A python library to operate Speed devices.

Currently the API has an unique backend allowing to control miniature devices like the Faller (c) Crane or DCC trains.

Examples
^^^^^^^^

Controlling a Faller (c) crane model
-------------------------------------

    >>> from speedlib.cranes import faller
    >>> from speedlib.cranes.faller import Crane
    >>> ip_1 = "172.17.217.217"
    >>> ip_2 = "172.17.217.217"
    >>> crane_1 = Crane()
    >>> crane_2 = Crane()
    >>> crane_1.init(ip_0)
    >>> crane_2.init(ip_2)
    >>> crane_2.start_for(20*faller.ureg.millisecond,faller.MotorChassis,faller.MotorDirectionForward)
    >>> crane_1.change_speed(faller.MotorCrab, -40)


Controlling a DCC train model
-----------------------------

    >>> from speedlib.dcc import dcc_object, dcc_trains
    >>> from speedlib.dcc.dcc_object import DCCObject
    >>>from speedlib.dcc .dcc_trains import Train

    >>> train = Train("DCC15",15)
    >>> dcc_object.start()
    >>> train.speed = 14
    >>> train.faster()
    >>> train.slower()
    >>> train.fl_light = True
    >>> print(train)
    >>> train.f2 = False
    >>> dcc_object.stop()

Controlling a DCC Switch model
-------------------------------

    >>> from speedlib.dcc import dcc_object, dcc_switches
    >>> from speedlib.dcc.dcc_object import DCCObject
    >>>from speedlib.dcc .dcc_switches import Switch

    >>> SS = Switch("DCC",3, 1)
    >>> dcc_object.start()
    >>> print(S.biais)
    >>> S.biais = True
    >>> S.set_biais_id(2)
    >>> S.biais = True
    >>> S.biais = False
    >>> dcc_object.stop()

You can find more examples in the *examples* directory.

Install
-------
git clone https://github.com/CRIStAL-PADR/Speed.git

The library is in speedlib/__init__.py

Tests
-----
To starts the unit tests you can do:

cd tests/
    >>> PYTHONPATH=../ python3 -m unittest
