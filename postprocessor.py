#Import relevant libraries
import serial
import numpy as np
import matplotlib.pyplot as plt 
from drawnow import *
import xlwt
import time

#Set 'recording' to true on startup
recording = True 
#Set counter to 0
cnt = 0

#Initialise serial port and flush buffer
data = serial.Serial('\dev\cu.usbmodem1421',115200)
data.flushInput()
data.flushOutput()
time = sleep(0.1)

#Initialise empty lists for data
hour=[]
minute=[]
seconds=[]
milliseconds=[]
speed=[]
latitude=[]
longitude=[]
frontTrav=[]
rearTrav=[]
frontBrake=[]
rearBrake=[]

#Initialise bottom-out counters at 0
BottomOutCntF = 0
BottomOutCntR = 0

#Initalise spreadsheet
bold = xlwt.easyxf('font: bold 1')
book = xlwt.Workbook(encoding='utf-8')
gpsSheet = book.add_sheet('GPS',cell_overwrite_ok=True)
gpsSheet.write(0,0,'Average Speed:',bold)
gpsSheet.write(2,0,'Max Speed:',bold)
gpsSheet.write(0,3,'Average Fork Sag (mm):',bold)
gpsSheet.write(1,3,'Fork Bottom-Outs:',bold)
gpsSheet.write(2,3,'Max Fork Travel (mm):',bold)
gpsSheet.write(0,5,'Average Shock Sag (mm):',bold)
gpsSheet.write(1,5,'Shock Bottom-Outs:',bold)
gpsSheet.write(2,5,'Max Shock Travel:',bold)
gpsSheet.write(4,0,'Time',bold)
gpsSheet.write(4,1,'Latitude',bold)
gpsSheet.write(4,2,'Speed',bold)
gpsSheet.write(4,3,'Front Suspension Travel (mm)',bold)
gpsSheet.write(4,4,'Rear Suspension Travel (mm)',bold)
gpsSheet.write(4,5,'Front Braking Force (N)',bold)
gpsSheet.write(4,6,'Rear Braking Force (N)',bold)

#Create the figure to display live data
def makeFig():

	#2x2 grid of plots
	plt.subplot(221)
	plt.plot(frontTrav)
	plt.title('Fork Travel')
	#Limit y-axis to total travel of fork, allow x-axis to adjust with time
	plt.ylim(0,160)
	plt.ylabel('Travel (mm)')

	plt.subplot(222)
	plt.plot(rearTrav)
	plt.title('Shock Travel')




























