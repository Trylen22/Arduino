/*
Thermistor Temperature Sensor Test
=================================

This sketch tests a thermistor temperature sensor to ensure it's working properly.
Connect the thermistor to analog pin A5.

Wiring:
- One terminal to 5V
- Other terminal to A5 (analog pin)
- 10kΩ resistor between A5 and GND

Author: [Your Name]
Date: [2025-01-27]
*/

const int THERMISTOR_PIN = A5;  // Thermistor on analog pin A5

// Thermistor calibration values (adjust based on your specific thermistor)
const float THERMISTOR_NOMINAL = 10000;  // Resistance at nominal temperature
const float TEMPERATURE_NOMINAL = 25;    // Nominal temperature (25°C)
const int BETA_COEFFICIENT = 3950;       // Beta coefficient
const float SERIES_RESISTANCE = 10000;   // Series resistance (10kΩ)

void setup() {
  Serial.begin(9600);
  Serial.println("Thermistor Temperature Sensor Test");
  Serial.println("==================================");
  Serial.println("This will continuously read temperature.");
  Serial.println("Expected values:");
  Serial.println("- Room temperature: ~20-25°C");
  Serial.println("- Body temperature: ~37°C");
  Serial.println();
}

void loop() {
  // Read the thermistor
  int thermistorValue = analogRead(THERMISTOR_PIN);
  
  // Convert to resistance
  float resistance = SERIES_RESISTANCE * ((1023.0 / thermistorValue) - 1.0);
  
  // Calculate temperature using Steinhart-Hart equation
  float steinhart = resistance / THERMISTOR_NOMINAL;
  steinhart = log(steinhart);
  steinhart /= BETA_COEFFICIENT;
  steinhart += 1.0 / (TEMPERATURE_NOMINAL + 273.15);
  steinhart = 1.0 / steinhart;
  steinhart -= 273.15;
  
  // Convert to Fahrenheit
  float fahrenheit = (steinhart * 9.0) / 5.0 + 32.0;
  
  // Print results
  Serial.print("Raw ADC: ");
  Serial.print(thermistorValue);
  Serial.print(" | Resistance: ");
  Serial.print(resistance, 0);
  Serial.print("Ω | Temperature: ");
  Serial.print(steinhart, 1);
  Serial.print("°C (");
  Serial.print(fahrenheit, 1);
  Serial.println("°F)");
  
  // Wait 2 seconds before next reading
  delay(2000);
} 