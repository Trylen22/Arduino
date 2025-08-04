/*
Environmental Monitoring System - Combined
========================================

This sketch combines all your working circuits:
- MQ-135 CO2 sensor (A0)
- Thermistor temperature sensor (A5) 
- Photoresistor light sensor (A2)
- LED indicator (pin 3)
- Fan control (pin 4)

Simple serial interface for LLM agent control.

Author: [Your Name]
Date: [2025-01-27]
*/

// Pin definitions
const int CO2_PIN = A0;           // MQ-135 CO2 sensor
const int THERMISTOR_PIN = A5;     // Thermistor temperature sensor
const int PHOTO_PIN = A2;          // Photoresistor light sensor
const int LED_PIN = 3;             // LED indicator
const int FAN_PIN = 4;             // Fan control

// Thermistor calibration (your improved equation)
const float TEMP_COEFF = 0.0916;
const float TEMP_OFFSET = -22.8683;

// Light level thresholds (calibrated for your photoresistor)
const int LIGHT_DARK = 200;        // Below this = dark
const int LIGHT_DIM = 400;         // Below this = dim
const int LIGHT_MODERATE = 600;    // Below this = moderate
const int LIGHT_BRIGHT = 800;      // Below this = bright
// Above 800 = very bright

// Temperature thresholds for automatic fan control
const float TEMP_HOT = 80.0;       // Turn fan on above this temperature
const float TEMP_COOL = 75.0;      // Turn fan off below this temperature

// Global variables
bool led_state = false;
bool fan_state = false;
String inputString = "";
bool stringComplete = false;

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  digitalWrite(FAN_PIN, LOW);
  
  Serial.println("Environmental Monitor Ready!");
  Serial.println("Available commands:");
  Serial.println("  'L1' - Turn LED ON");
  Serial.println("  'L0' - Turn LED OFF");
  Serial.println("  'F1' - Turn Fan ON");
  Serial.println("  'F0' - Turn Fan OFF");
  Serial.println("  'S' - Status report (all sensors)");
  Serial.println("  'T' - Temperature only");
  Serial.println("  'C' - CO2 only");
  Serial.println("  'P' - Light level only");
  Serial.println("  'A' - All sensor readings");
  Serial.println();
}

void loop() {
  // Check for serial commands
  if (stringComplete) {
    processCommand(inputString);
    inputString = "";
    stringComplete = false;
  }
  
  delay(10);
}

// Serial event handler
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

// Process incoming commands
void processCommand(String command) {
  command.trim();
  
  if (command == "L1") {
    turnLEDOn();
  } else if (command == "L0") {
    turnLEDOff();
  } else if (command == "F1") {
    turnFanOn();
  } else if (command == "F0") {
    turnFanOff();
  } else if (command == "S") {
    sendStatusReport();
  } else if (command == "T") {
    sendTemperatureOnly();
  } else if (command == "C") {
    sendCO2Only();
  } else if (command == "P") {
    sendLightOnly();
  } else if (command == "A") {
    sendAllReadings();
  } else {
    Serial.println("Unknown command: " + command);
  }
}

// LED control functions
void turnLEDOn() {
  digitalWrite(LED_PIN, HIGH);
  led_state = true;
  Serial.println("LED: ON");
}

void turnLEDOff() {
  digitalWrite(LED_PIN, LOW);
  led_state = false;
  Serial.println("LED: OFF");
}

// Fan control functions
void turnFanOn() {
  digitalWrite(FAN_PIN, HIGH);
  fan_state = true;
  Serial.println("FAN: ON");
}

void turnFanOff() {
  digitalWrite(FAN_PIN, LOW);
  fan_state = false;
  Serial.println("FAN: OFF");
}

// Sensor reading functions
float readTemperature() {
  int rawValue = analogRead(THERMISTOR_PIN);
  float tempC = TEMP_COEFF * rawValue + TEMP_OFFSET;
  float tempF = (tempC * 9.0 / 5.0) + 32.0;
  return tempF;
}

int readCO2() {
  int rawValue = analogRead(CO2_PIN);
  return rawValue;
}

int readLight() {
  int rawValue = analogRead(PHOTO_PIN);
  return rawValue;
}

// Brightness interpretation function
String getBrightnessDescription(int lightValue) {
  if (lightValue < LIGHT_DARK) {
    return "Very Dark";
  } else if (lightValue < LIGHT_DIM) {
    return "Dark";
  } else if (lightValue < LIGHT_MODERATE) {
    return "Dim";
  } else if (lightValue < LIGHT_BRIGHT) {
    return "Moderate";
  } else if (lightValue < 1000) {
    return "Bright";
  } else {
    return "Very Bright";
  }
}

// Get light level percentage (0-100)
int getLightPercentage(int lightValue) {
  // Assuming max value is around 1023 (10-bit ADC)
  // Adjust these values based on your photoresistor's range
  int maxLight = 1023;
  int minLight = 0;
  
  int percentage = map(lightValue, minLight, maxLight, 0, 100);
  return constrain(percentage, 0, 100); // Ensure it's between 0-100
}

// Status reporting functions
void sendStatusReport() {
  float temp = readTemperature();
  int co2 = readCO2();
  int light = readLight();
  String brightness = getBrightnessDescription(light);
  int lightPercent = getLightPercentage(light);
  
  Serial.println("=== STATUS REPORT ===");
  Serial.print("LED: ");
  Serial.println(led_state ? "ON" : "OFF");
  Serial.print("Fan: ");
  Serial.println(fan_state ? "ON" : "OFF");
  Serial.print("Temperature: ");
  Serial.print(temp, 1);
  Serial.println("°F");
  Serial.print("CO2: ");
  Serial.println(co2);
  Serial.print("Light: ");
  Serial.print(light);
  Serial.print(" (");
  Serial.print(brightness);
  Serial.print(", ");
  Serial.print(lightPercent);
  Serial.println("% brightness)");
  Serial.println("===================");
}

void sendTemperatureOnly() {
  float temp = readTemperature();
  Serial.print("TEMP:");
  Serial.println(temp, 1);
}

void sendCO2Only() {
  int co2 = readCO2();
  Serial.print("CO2:");
  Serial.println(co2);
}

void sendLightOnly() {
  int light = readLight();
  String brightness = getBrightnessDescription(light);
  int lightPercent = getLightPercentage(light);
  
  Serial.print("LIGHT:");
  Serial.print(light);
  Serial.print(",");
  Serial.print(brightness);
  Serial.print(",");
  Serial.println(lightPercent);
}

void sendAllReadings() {
  float temp = readTemperature();
  int co2 = readCO2();
  int light = readLight();
  String brightness = getBrightnessDescription(light);
  int lightPercent = getLightPercentage(light);
  
  Serial.print("ALL:");
  Serial.print(temp, 1);
  Serial.print(",");
  Serial.print(co2);
  Serial.print(",");
  Serial.print(light);
  Serial.print(",");
  Serial.print(brightness);
  Serial.print(",");
  Serial.print(lightPercent);
  Serial.print(",");
  Serial.print(led_state ? "1" : "0");
  Serial.print(",");
  Serial.println(fan_state ? "1" : "0");
} 