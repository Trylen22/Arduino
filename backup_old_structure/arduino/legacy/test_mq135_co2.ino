/*
MQ-135 CO2 Sensor Test
======================

This sketch tests the MQ-135 CO2 sensor to ensure it's working properly.
Connect the MQ-135 sensor to analog pin A0.

Wiring:
- VCC to 5V
- GND to GND  
- AOUT to A0 (analog pin)

Author: [Your Name]
Date: [2025-01-27]
*/

const int MQ135_PIN = A0;  // MQ-135 sensor on analog pin A0

// MQ-135 calibration values (adjust based on your specific sensor)
const float MQ135_RL = 10000;  // Load resistance
const float MQ135_RO = 10000;  // Sensor resistance in clean air

void setup() {
  Serial.begin(9600);
  Serial.println("MQ-135 CO2 Sensor Test");
  Serial.println("=======================");
  Serial.println("This will continuously read CO2 levels.");
  Serial.println("Expected values:");
  Serial.println("- Clean air: ~400 ppm");
  Serial.println("- Poor ventilation: 800-1000 ppm");
  Serial.println("- Very poor: 1000+ ppm");
  Serial.println();
}

void loop() {
  // Read the sensor
  int rawValue = analogRead(MQ135_PIN);
  float voltage = (rawValue / 1024.0) * 5.0;
  
  // Calculate resistance
  float rs = ((5.0 * MQ135_RL) / voltage) - MQ135_RL;
  float ratio = rs / MQ135_RO;
  
  // Calculate CO2 concentration (simplified)
  float co2_ppm = 116.6020682 * pow(ratio, -1.769647925);
  
  // Print results
  Serial.print("Raw ADC: ");
  Serial.print(rawValue);
  Serial.print(" | Voltage: ");
  Serial.print(voltage, 2);
  Serial.print("V | Resistance: ");
  Serial.print(rs, 0);
  Serial.print("Ω | CO2: ");
  Serial.print(co2_ppm, 0);
  Serial.println(" ppm");
  
  // Wait 2 seconds before next reading
  delay(2000);
} 