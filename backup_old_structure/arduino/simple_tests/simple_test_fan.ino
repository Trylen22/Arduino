/*
Simple Fan Test
===============

Basic test for fan control on pin 8.
Just turns fan on and off with serial feedback.

Wiring:
- Transistor base to pin 8 through 1kΩ resistor
- Transistor collector to fan positive
- Transistor emitter to GND
- Fan negative to GND
*/

const int FAN_PIN = 4;

void setup() {
  Serial.begin(9600);
  pinMode(FAN_PIN, OUTPUT);
  Serial.println("Fan Test - Pin 4");
}

void loop() {
  // Turn Fan ON
  digitalWrite(FAN_PIN, HIGH);
  Serial.println("Fan ON");
  delay(3000);
  
  // Turn Fan OFF
  digitalWrite(FAN_PIN, LOW);
  Serial.println("Fan OFF");
  delay(3000);
} 