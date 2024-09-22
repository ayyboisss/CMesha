int sensorPin =A0 ;  // define analog port A0
int value = 0;    //set value to 0
void setup() 
{
 Serial.begin(9600); //set the baud rate to 9600
} 
void loop() 
{
value = analogRead(sensorPin);  //set the value as the value read from A0
Serial.println(value, DEC);  //print the value and line wrap
delay(500);  //delay 0.2S
} 
