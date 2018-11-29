#Import relevant libraries
import serial
import numpy as np
import matplotlib.pyplot as plt 
from drawnow import *
import xlwt
import time

#Set 'recording' to true on startup
recording = True 
#Set index to 0
i = 0

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
bottomOutCntF = 0
bottomOutCntR = 0

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
	plt.ylim(0,65)
	plt.ylabel('Travel (mm)')

	plt.subplot(223)
	plt.plot(frontBrake)
	plt.title('Front Brake Force')
	plt.ylim(0,4000)
	plt.ylabel('Force (N)')

	plt.subplot(224)
	plt.plot(rearBrake)
	plt.title('Rear Brake Force')
	plt.ylim(0,4000)
	ply.ylabel('Force (N)')

#Write to spreadsheet
def writeExcel():

	#Call counters; global variables
	global i
	global bottomOutCntF
	global bottomOutCntR

	#Calculate average and max speed
	avgSpeed = np.mean(speed)
	maxSpeed = max(speed)
	#Calculate average sag, front and rear
	avgSagF = np.mean(frontTrav)
	avgSagR = np.mean(rearTrav)
	#Calculate maximum travel utilisation
	maxTravF = max(frontTrav)
	maxTravR = max(rearTrav)

	#Increment bottom-out counters if required
	if(frontTrav[i] >= 155):
		BottomOutCntF = BottomOutCntF+1
	if(rearTrav[i] >= 60):
		bottomOutCntR = BottomOutCntR+1

	#Write calculated values to sheet
	gpsSheet.write(0,1,avgSpeed)
	gpsSheet.write(2,1,maxSpeed)
	gpsSheet.write(0,4,avgSagF)
	gpsSheet.write(1,4,bottomOutCntF)
	gpsSheet.write(2,4,maxTravF)
	gpsSheet.write(0,6,avgSagR)
	gpsSheet.write(1,6,bottomOutCntR)
	gpsSheet.write(2,6,maxTravR)

	#Write the current data to the sheet
	gpsSheet.write(i+5,0,'{:d}:{:d}:{:d}:{:d}'.format(hour[i],minute[i],seconds[i],milliseconds[i]))
	gpsSheet.write(i+5,1,latitude[i])
	gpsSheet.write(i+5,2,longitude[i])
	gpsSheet.write(i+5,3,speed[i])
	gpsSheet.write(i+5,4,frontTrav[i])
	gpsSheet.write(i+5,5,rearTrav[i])
	gpsSheet.write(i+5,6,frontBrake[i])
	gpsSheet.write(i+5,7,rearBrake[i])

	#Save sheet
	book.save('data.xls')

	#Increment index
	i = i+1

#Main loop
while recording:

	#Read raw string from arduino serial port
	line = data.readline()

	print line #Uncomment for debugging

	#Split line at commas
	dataArray = line.split(',')

	#Line of data from arduino should begin with $
	#To prevent corrupt data from being processed, check for $ at index 0
	if dataArray[0] == '$':

		#Remove verification character
		dataArray.pop(0)

		#Add current data to lists
		hour.append(int(dataArray[0]))
		minute.append(int(dataArray[1]))
		seconds.append(int(dataArray[2]))
		milliseconds.append(int(dataArray[3]))
		latitude.append(float(dataArray[4]))
		longitude.append(float(dataArray[5]))
		speed.append(float(dataArray[6]))
		#Values for suspension travel and braking force must be converted to mm/N
		frontBrake.append(2.71828**((int(dataArray[7])+1283)/266.06))
		rearBrake.append(2.71828**((int(dataArray[8])+1283)/266.06))
		frontTrav.append((int(dataArray[9])-155.53)/5.1)
		rearTrav.append(int(dataArray[10])/11.042)

		#Update the figure
		drawnow(makeFig)
		#Pause for stability
		plt.pause(0.000001)
		#Update spreadsheet
		writeExcel()
































