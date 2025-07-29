/*
LED Indicator Test
==================

This sketch tests an LED indicator to ensure it's working properly.
Connect the LED to digital pin 3.

Wiring:
- LED positive (longer leg) to pin 3
- LED negative (shorter leg) to GND through a 220Ω resistor

Author: [Your Name]
Date: [2025-01-27]
*/

const int LED_PIN = 3;  // LED on digital pin 3

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  
  Serial.println("LED Indicator Test");
  Serial.println("==================");
  Serial.println("This will cycle the LED through different patterns.");
  Serial.println("Commands:");
  Serial.println("  '1' - Turn LED ON");
  Serial.println("  '0' - Turn LED OFF");
  Serial.println("  'B' - Blink pattern");
  Serial.println("  'F' - Fade pattern");
  Serial.println();
}

void loop() {
  // Check for serial commands
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    switch (command) {
      case '1':
        digitalWrite(LED_PIN, HIGH);
        Serial.println("LED: ON");
        break;
        
      case '0':
        digitalWrite(LED_PIN, LOW);
        Serial.println("LED: OFF");
        break;
        
      case 'B':
        blinkPattern();
        break;
        
      case 'F':
        fadePattern();
        break;
        
      default:
        Serial.println("Unknown command. Use 1, 0, B, or F");
        break;
    }
  }
  
  delay(100);
}

void blinkPattern() {
  Serial.println("Starting blink pattern...");
  for (int i = 0; i < 5; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(500);
    digitalWrite(LED_PIN, LOW);
    delay(500);
  }
  Serial.println("Blink pattern complete!");
}

void fadePattern() {
  Serial.println("Starting fade pattern...");
  
  // Fade in
  for (int brightness = 0; brightness <= 255; brightness++) {
    analogWrite(LED_PIN, brightness);
    delay(10);
  }
  
  // Fade out
  for (int brightness = 255; brightness >= 0; brightness--) {
    analogWrite(LED_PIN, brightness);
    delay(10);
  }
  
  Serial.println("Fade pattern complete!");
} 