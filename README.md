# MTB-telemetry

The software for a telemetry system for downhill mountain bikes.

## transmitter.ino

The embedded software for the hardware mounted on the bike. Takes in data from the onboard array of sensors and transmits via radio module.

## reciever.ino

Embedded software for reciever plugged into laptop. Parses data transmitted from the on-board hardware and sends to the post-processor via the serial port of the arduino.

## postprocessor.py

Basic post-processing software written in Python 2.7; displays data from sensors in real time and writes to a spreadsheet.