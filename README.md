# FGFSControllerWeb

A website that allows an iPhone to controls a flight simulator
 ([FGFS](https://www.flightgear.org/)) on a computer.

* Aileron, elevator, rudder, and throttle can be controlled.

* Data are collected through accelerometer in the iOS device, and transmitted
 using HTTPS GET / Web Socket to the server. The server sends UDP packets to
 FGFS.

* This project is based on
 [FGFS-Controller](https://github.com/lxylxy123456/FGFS-Controller) (an iOS app)

## TODO
* Debug web socket on safari.

## Demo
[![YxqSxod6d7o](http://img.youtube.com/vi/YxqSxod6d7o/0.jpg)](http://www.youtube.com/watch?v=YxqSxod6d7o)

Screenshot:

![FGFSControllerWeb1.png](https://lxylxy123456.github.io/image/FGFSControllerWeb1.png)

A new throttle control UI:

![FGFSControllerWeb2.png](https://lxylxy123456.github.io/image/FGFSControllerWeb2.png)

Receiver (made with pygame):

![FGFSControllerWeb3.png](https://lxylxy123456.github.io/image/FGFSControllerWeb3.png)

