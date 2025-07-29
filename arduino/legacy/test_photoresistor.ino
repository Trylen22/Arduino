/*
Photoresistor Light Sensor Test
===============================

This sketch tests a photoresistor light sensor to ensure it's working properly.
Connect the photoresistor to analog pin A2.

Wiring:
- One terminal to 5V
- Other terminal to A2 (analog pin)
- 10kΩ resistor between A2 and GND

Author: [Your Name]
Date: [2025-01-27]
*/

const int PHOTORESISTOR_PIN = A2;  // Photoresistor on analog pin A2

void setup() {
  Serial.begin(9600);
  Serial.println("Photoresistor Light Sensor Test");
  Serial.println("================================");
  Serial.println("This will continuously read light levels.");
  Serial.println("Expected values:");
  Serial.println("- Bright light: 800-1023");
  Serial.println("- Normal room light: 400-800");
  Serial.println("- Low light: 200-400");
  Serial.println("- Dark: 0-200");
  Serial.println();
}

void loop() {
  // Read the photoresistor
  int lightValue = analogRead(PHOTORESISTOR_PIN);
  
  // Convert to voltage
  float voltage = (lightValue / 1024.0) * 5.0;
  
  // Determine light level description
  String lightLevel;
  if (lightValue > 800) {
    lightLevel = "Very Bright";
  } else if (lightValue > 600) {
    lightLevel = "Bright";
  } else if (lightValue > 400) {
    lightLevel = "Normal";
  } else if (lightValue > 200) {
    lightLevel = "Dim";
  } else {
    lightLevel = "Dark";
  }
  
  // Print results
  Serial.print("Raw ADC: ");
  Serial.print(lightValue);
  Serial.print(" | Voltage: ");
  Serial.print(voltage, 2);
  Serial.print("V | Light Level: ");
  Serial.print(lightLevel);
  Serial.print(" (");
  Serial.print(lightValue);
  Serial.println(")");
  
  // Wait 1 second before next reading
  delay(1000);
} 