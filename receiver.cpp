#include <SPI.h>
#include <RF24.h>

//Create radio object on pins 7 and 8
RF24 radio(7,8);

//Set address to receive data
const byte address[6] = "00001";

//Create structure to receive data
typedef struct
{
	
	float latitude;
	float longitude;
	float speed;
	int hour;
	int minute;
	int seconds;
	int milliseconds;
	int FBForce;
	int RBForce;
	int frontTrav;
	int rearTrav;

}
B_t;

B_t receive;

void setup() {

	//Start serial monitor
	Serial.begin(115200);

	//Initailise radio
	radio.begin();
	radio.openReadingPipe(0,address);
	radio.setPALevel(RF24_PA_MIN);
	radio.setDataRate(RF24_250KBPS);
	radio.setChannel(124);
	radio.startListening();

}

void loop() {

	if(radio.available()){

		//Receive radio data
		radio.read(&receive,sizeof(receive));

		//Write to serial monitor
		Serial.print("$"); //Validation character to prevent postprocessor from taking corrupt data
		Serial.print(receive.hour,DEC);
		Serial.print(",");
		if(receive.minute <= 9){
			Serial.print("0");
		}
		Serial.print(receive.minute,DEC);
		Serial.print(",");
		if(receive.seconds <= 9){
			Serial.print("0");
		}
		Serial.print(receive.seconds,DEC);
		Serial.print(",");
		if(receive.milliseconds <= 9){
			Serial.print("0");
		}
		if(receive.milliseconds <= 99){
			Serial.print("0");
		}
		Serial.print(receive.milliseconds);
		Serial.print(",");
		Serial.print(receive.latitude);
		Serial.print(",");
		Serial.print(receive.longitude);
		Serial.print(",");
		Serial.print(receive.speed);
		Serial.print(",");
		Serial.print(receive.frontTrav);
		Serial.print(",");
		Serial.print(receive.rearTrav);
		Serial.print(",");
		Serial.print(receive.FBForce);
		Serial.print(",");
		Serial.println(recieve.RBForce);

	}
}


















