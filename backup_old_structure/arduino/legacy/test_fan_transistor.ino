/*
Transistor-Controlled Fan Test
==============================

This sketch tests a transistor-controlled fan to ensure it's working properly.
Connect the transistor base to digital pin 8.

Wiring:
- Transistor base to pin 8 through a 1kΩ resistor
- Transistor collector to fan positive
- Transistor emitter to GND
- Fan negative to GND
- 12V power supply for fan (if needed)

Author: [Your Name]
Date: [2025-01-27]
*/

const int FAN_PIN = 8;  // Transistor base on digital pin 8

void setup() {
  Serial.begin(9600);
  pinMode(FAN_PIN, OUTPUT);
  
  Serial.println("Transistor-Controlled Fan Test");
  Serial.println("==============================");
  Serial.println("This will test the fan control circuit.");
  Serial.println("Commands:");
  Serial.println("  '1' - Turn Fan ON");
  Serial.println("  '0' - Turn Fan OFF");
  Serial.println("  'P' - Pulse pattern");
  Serial.println("  'S' - Speed test");
  Serial.println();
}

void loop() {
  // Check for serial commands
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    switch (command) {
      case '1':
        digitalWrite(FAN_PIN, HIGH);
        Serial.println("Fan: ON");
        break;
        
      case '0':
        digitalWrite(FAN_PIN, LOW);
        Serial.println("Fan: OFF");
        break;
        
      case 'P':
        pulsePattern();
        break;
        
      case 'S':
        speedTest();
        break;
        
      default:
        Serial.println("Unknown command. Use 1, 0, P, or S");
        break;
    }
  }
  
  delay(100);
}

void pulsePattern() {
  Serial.println("Starting pulse pattern...");
  for (int i = 0; i < 5; i++) {
    digitalWrite(FAN_PIN, HIGH);
    delay(1000);
    digitalWrite(FAN_PIN, LOW);
    delay(1000);
  }
  Serial.println("Pulse pattern complete!");
}

void speedTest() {
  Serial.println("Starting speed test...");
  
  // Test different speeds using PWM
  for (int speed = 0; speed <= 255; speed += 51) {
    analogWrite(FAN_PIN, speed);
    Serial.print("Fan speed: ");
    Serial.print(speed);
    Serial.println("/255");
    delay(2000);
  }
  
  // Turn off
  digitalWrite(FAN_PIN, LOW);
  Serial.println("Speed test complete!");
} 