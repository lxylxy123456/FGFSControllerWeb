# FGFS-Controller

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

