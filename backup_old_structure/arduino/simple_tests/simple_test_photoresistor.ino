/*
Simple Photoresistor Test
=========================

Basic test for photoresistor on pin A2.
Just prints raw analog values.

Wiring:
- One terminal to 5V
- Other terminal to A2
- 10kΩ resistor between A2 and GND
*/

const int PHOTO_PIN = A2;

void setup() {
  Serial.begin(9600);
  Serial.println("Photoresistor Test - Pin A2");
}

void loop() {
  int rawValue = analogRead(PHOTO_PIN);
  Serial.print("Light Raw: ");
  Serial.println(rawValue);
  delay(1000);
} 