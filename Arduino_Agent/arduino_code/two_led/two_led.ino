/*
Two LED Control Arduino Code
===========================

This Arduino code controls two LEDs based on serial commands from the Python agent.
The system responds to simple character commands to control LED states.

Author: [Your Name]
Date: [2025-01-27]
*/

// ===== PIN DEFINITIONS =====
const int LED1_PIN = 13;  // LED 1 connected to pin 13
const int LED2_PIN = 12;  // LED 2 connected to pin 12

// ===== GLOBAL VARIABLES =====
bool led1_state = false;  // Track LED 1 state
bool led2_state = false;  // Track LED 2 state
String inputString = "";   // String to hold incoming data
bool stringComplete = false;  // Whether the string is complete

// ===== SETUP FUNCTION =====
void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Set LED pins as outputs
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  
  // Initialize LEDs to OFF state
  digitalWrite(LED1_PIN, LOW);
  digitalWrite(LED2_PIN, LOW);
  
  // Send startup message
  Serial.println("Two LED Controller Ready!");
  Serial.println("Available commands:");
  Serial.println("  '1' - Turn LED 1 ON");
  Serial.println("  'a' - Turn LED 1 OFF");
  Serial.println("  '2' - Turn LED 2 ON");
  Serial.println("  'b' - Turn LED 2 OFF");
  Serial.println("  '3' - Turn both LEDs ON");
  Serial.println("  'c' - Turn both LEDs OFF");
  Serial.println("  'S' - Status report");
  Serial.println("  't1' - Toggle LED 1");
  Serial.println("  't2' - Toggle LED 2");
  Serial.println();
}

// ===== MAIN LOOP =====
void loop() {
  // Check if we have received a complete command
  if (stringComplete) {
    // Process the command
    processCommand(inputString);
    
    // Clear the string for next command
    inputString = "";
    stringComplete = false;
  }
  
  // Small delay to prevent overwhelming the serial buffer
  delay(10);
}

// ===== SERIAL EVENT HANDLER =====
void serialEvent() {
  while (Serial.available()) {
    // Get the new byte
    char inChar = (char)Serial.read();
    
    // Add it to the inputString
    inputString += inChar;
    
    // If the incoming character is a newline, set a flag
    // so the main loop can do something about it
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

// ===== COMMAND PROCESSING =====
void processCommand(String command) {
  // Remove any whitespace and newlines
  command.trim();
  
  // Process single character commands
  if (command.length() == 1) {
    char cmd = command.charAt(0);
    
    switch (cmd) {
      case '1':  // Turn LED 1 ON
        turnLED1On();
        break;
        
      case 'a':  // Turn LED 1 OFF
        turnLED1Off();
        break;
        
      case '2':  // Turn LED 2 ON
        turnLED2On();
        break;
        
      case 'b':  // Turn LED 2 OFF
        turnLED2Off();
        break;
        
      case '3':  // Turn both LEDs ON
        turnBothLEDsOn();
        break;
        
      case 'c':  // Turn both LEDs OFF
        turnBothLEDsOff();
        break;
        
      case 'S':  // Status report
        sendStatusReport();
        break;
        
      default:
        Serial.println("Unknown command: " + command);
        break;
    }
  }
  // Process two character commands (for toggles)
  else if (command.length() == 2) {
    if (command == "t1") {
      toggleLED1();
    }
    else if (command == "t2") {
      toggleLED2();
    }
    else {
      Serial.println("Unknown command: " + command);
    }
  }
  else {
    Serial.println("Invalid command format: " + command);
  }
}

// ===== LED CONTROL FUNCTIONS =====

void turnLED1On() {
  digitalWrite(LED1_PIN, HIGH);
  led1_state = true;
  Serial.println("LED 1: ON");
}

void turnLED1Off() {
  digitalWrite(LED1_PIN, LOW);
  led1_state = false;
  Serial.println("LED 1: OFF");
}

void turnLED2On() {
  digitalWrite(LED2_PIN, HIGH);
  led2_state = true;
  Serial.println("LED 2: ON");
}

void turnLED2Off() {
  digitalWrite(LED2_PIN, LOW);
  led2_state = false;
  Serial.println("LED 2: OFF");
}

void turnBothLEDsOn() {
  digitalWrite(LED1_PIN, HIGH);
  digitalWrite(LED2_PIN, HIGH);
  led1_state = true;
  led2_state = true;
  Serial.println("Both LEDs: ON");
}

void turnBothLEDsOff() {
  digitalWrite(LED1_PIN, LOW);
  digitalWrite(LED2_PIN, LOW);
  led1_state = false;
  led2_state = false;
  Serial.println("Both LEDs: OFF");
}

void toggleLED1() {
  if (led1_state) {
    turnLED1Off();
  } else {
    turnLED1On();
  }
}

void toggleLED2() {
  if (led2_state) {
    turnLED2Off();
  } else {
    turnLED2On();
  }
}

// ===== STATUS REPORTING =====
void sendStatusReport() {
  Serial.println("=== STATUS REPORT ===");
  Serial.print("LED 1: ");
  Serial.println(led1_state ? "ON" : "OFF");
  Serial.print("LED 2: ");
  Serial.println(led2_state ? "ON" : "OFF");
  Serial.println("===================");
}