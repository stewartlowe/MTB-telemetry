//Libraries for SD card
#include <SD.h>
#include <SPI.h>
//Libraries for GPS
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

//Begin software serial on pins 7 and 8
SoftwareSerial mySerial(8,7);
Adafruit_GPS GPS(&mySerial);

//Strings for storing NMEA sentances
String NMEA1;
String NMEA2;
//Char for reading data stream from GPS
char c;
//CS pin on SD
int chipSelect = 10;
//File object for SD
File sensorData;

void setup() {

	Serial.begin(115200);

	//Initialise GPS
	GPS.begin(9600);
	GPS.sendCommand("$PGCMD,33,0*6D"); //Stop antenna update info
	GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA); //Stream RMC and GGA sentances
	GPS.sendCommand(PMTK_SET_NMEA_UPDATE_10HZ);

	//Initialise SD card
	SD.begin(chipSelect);
	if(SD.exists("CSVData.txt")){
		SD.remove("CSVData.txt");
	}
	if(SD.exists("NMEAraw.txt")){
		SD.remove("NMEAraw.txt");
	}

	delay(1000);

}

void loop() {

	readGPS();

	if(GPS.fix==1){ //Only write data when GPS is working

		//Write to file of raw NMEA sentances
		sensorData = SD.open("NMEAraw.txt",FILE_WRITE);
		sensorData.println(NMEA1);
		sensorData.println(NMEA2);
		sensorData.close();

		//Write to file of coordinates
		sensorData = SD.open("CSVData.txt",FILE_WRITE);
		if(GPS.hour <= 9){
			sensorData.print("0");
		}
		sensorData.print(GPS.hour,DEC);
		sensorData.print(":");
		if(GPS.minute <= 9){
			sensorData.print("0");
		}
		sensorData.print(GPS.minute,DEC);
		sensorData.print(":");
		if(GPS.seconds <= 9){
			sensorData.print("0");
		}
		sensorData.print(GPS.seconds,DEC);
		sensorData.print(",");
		sensorData.print(GPS.latitudeDegrees,8);
		sensorData.print(",");
		sensorData.print(GPS.longitudeDegrees,8);
		sensorData.print(",");
		sensorData.println(GPS.altitude,8);
		sensorData.close();

	}
}

void readGPS() {
	//First NMEA sentance
	while(!GPS.newNMEAreceived()){
		c = GPS.read();
	}

	GPS.parse(GPS.lastNMEA());
	NMEA1 = GPS.lastNMEA();

	//Second NMEA sentance
	while(!GPS.newNMEAreceived()){
		c = GPS.read();
	}

	GPS.parse(GPS.lastNMEA());
	NMEA1 = GPS.lastNMEA();
}























