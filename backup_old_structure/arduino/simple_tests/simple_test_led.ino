/*
Simple LED Test
===============

Basic test for LED on pin 3.
Just turns LED on and off with serial feedback.

Wiring:
- LED positive to pin 3
- LED negative to GND through 220Ω resistor
*/

const int LED_PIN = 3;

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("LED Test - Pin 3");
}

void loop() {
  // Turn LED ON
  digitalWrite(LED_PIN, HIGH);
  Serial.println("LED ON");
  delay(2000);
  
  // Turn LED OFF
  digitalWrite(LED_PIN, LOW);
  Serial.println("LED OFF");
  delay(2000);
} 