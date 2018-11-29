#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>
#include <SPI.h>
#include <RF24.h>

//Name sensor input pins
int frontBrake = A0;
int rearBrake = A1;
int fork = A2;
int shock = A3;

//Define variable to store and read NMEA sentance from GPS 
String NMEA;
char c;

//Initialise Software Serial and create GPS object
SoftwareSerial mySerial(8,7);
Adafruit_GPS GPS(&mySerial);
//Create radio object
RF24 radio(2,3);

//Address to transmit
const byte address[6] = "00001";

void setup() {

	//Begin serial port for debugging, comment when system in use
	Serial.begin(9600);

	//Initialise the GPS module
	GPS.begin(9600);
	GPS.sendCommand("$PGCMD,33,0*6D"); //Command to suppress antenna status
	GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY); //Only stream RMC sentances
	GPS.sendCommand(PMTK_SET_NMEA_UPDATE_10HZ); //Set module to maximum refresh rate (10Hz)

	//Initialise radio
	radio.begin();
	radio.openWritingPipe(address);
	radio.setPALevel(RF_PA_MIN);
	radio.setDataRate(RF24_250KBPS);
	radio.setChannel(124);
	radio.stopListening();

	//Initialise input pins
	pinMode(frontBrake,INPUT);
	pinMode(rearBrake,INPUT);
	pinMode(fork,INPUT);
	pinMode(shock,INPUT);

	//Random seed for testing when sensors unavailable
	randomSeed(analogRead(0));

	//Delay for stability
	delay(1000);

}

void loop() {

	readGPS();

	//Create data structure to be transmitted
	typedef struct 
	{
	
		float latitude = GPS.latitudeDegrees;
		float longitude = GPS.longitudeDegrees;
		float speed = GPS.speed;
		int hour = GPS.hour;
		int minute = GPS.minute;
		int seconds = GPS.seconds;
		int milliseconds = GPS.milliseconds;
		int FBForce = analogRead(frontBrake);
		int RBForce = analogRead(rearBrake):
		int frontTrav = analogRead(fork);
		int rearTrav = analogRead(shock);

		//Use the random values for sensor data when sensors are unavailable
		/*int FBForce = random(850);
		int RBForce = random(850);
		int frontTrav = random(159,975);
		int rearTrav = random(689);*/

	}
	A_t;

	A_t transmit;

	//Transmit data
	radio.write(&transmit,sizeof(transmit));

	Serial.println("Transmitting...");

}

void readGPS() {

	//Read characters until a complete NMEA is seen
	while (!GPS.newNMEAreceived()) {
		c = GPS.read();
	}
	GPS.parse(GPS.lastNMEA()); //Parse NMEA sentance
	NMEA = GPS.lastNMEA(); //Needed?
}

































