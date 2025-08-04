/*
Simple CO2 Sensor Test
======================

Basic test for MQ-135 CO2 sensor on pin A0.
Just prints raw analog values.

Wiring:
- VCC to 5V
- GND to GND
- AOUT to A0
*/

const int CO2_PIN = A0;

void setup() {
  Serial.begin(9600);
  Serial.println("CO2 Sensor Test - Pin A0");
}

void loop() {
  int rawValue = analogRead(CO2_PIN);
  Serial.print("CO2 Raw: ");
  Serial.println(rawValue);
  delay(1000);
} 