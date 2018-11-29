//Name input pin
int input = A0;
//Create output variable
int output;

void setup() {
	//Initialise input pin
	pinMode(input,INPUT);
	//Begin serial monitor
	Serial.begin(9600);
}

void loop() {
	output = analogRead(input);
	Serial.println(output);
	delay(100);
}