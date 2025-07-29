/*
Simple Thermistor Test
======================

Basic test for thermistor on pin A5.
Uses your improved calibration equation: TempC = 0.0916 * TempA - 22.8683

Wiring:
- One terminal to 5V
- Other terminal to A5
- 10kΩ resistor between A5 and GND
*/

const int THERMISTOR_PIN = A5;

void setup() {
  Serial.begin(9600);
  Serial.println("Thermistor Test - Pin A5");
  Serial.println("Using your improved calibration: TempC = 0.0916 * TempA - 22.8683");
}

void loop() {
  int rawValue = analogRead(THERMISTOR_PIN);
  
  // Use your improved calibration equation
  float tempC = 0.0916 * rawValue - 22.8683;
  float tempF = (9.0 / 5.0) * tempC + 32.0;
  
  Serial.print("Raw: ");
  Serial.print(rawValue);
  Serial.print(" | Temp: ");
  Serial.print(tempC, 1);
  Serial.print("°C (");
  Serial.print(tempF, 1);
  Serial.println("°F)");
  
  delay(1000);
} 