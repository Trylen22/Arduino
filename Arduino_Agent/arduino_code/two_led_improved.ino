/*
Red & Green LED Control Arduino Code
===================================

This Arduino code controls a red LED and a green LED based on serial commands from the Python agent.
The system responds to simple character commands to control LED states.

Author: [Your Name]
Date: [2025-01-27]
*/

// ===== PIN DEFINITIONS =====
const int RED_LED_PIN = 7;    // Red LED connected to pin 7
const int GREEN_LED_PIN = 11;  // Green LED connected to pin 11

// ===== GLOBAL VARIABLES =====
bool red_led_state = false;    // Track Red LED state
bool green_led_state = false;  // Track Green LED state
String inputString = "";       // String to hold incoming data
bool stringComplete = false;   // Whether the string is complete

// ===== SETUP FUNCTION =====
void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Set LED pins as outputs
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  
  // Initialize LEDs to OFF state
  digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(GREEN_LED_PIN, LOW);
  
  // Send startup message
  Serial.println("Red & Green LED Controller Ready!");
  Serial.println("Available commands:");
  Serial.println("  '1' - Turn Red LED ON");
  Serial.println("  'a' - Turn Red LED OFF");
  Serial.println("  '2' - Turn Green LED ON");
  Serial.println("  'b' - Turn Green LED OFF");
  Serial.println("  '3' - Turn both LEDs ON");
  Serial.println("  'c' - Turn both LEDs OFF");
  Serial.println("  'S' - Status report");
  Serial.println("  't1' - Toggle Red LED");
  Serial.println("  't2' - Toggle Green LED");
  Serial.println("  'D' - Delay command (D followed by milliseconds)");
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
      case '1':  // Turn Red LED ON
        turnRedLEDOn();
        break;
        
      case 'a':  // Turn Red LED OFF
        turnRedLEDOff();
        break;
        
      case '2':  // Turn Green LED ON
        turnGreenLEDOn();
        break;
        
      case 'b':  // Turn Green LED OFF
        turnGreenLEDOff();
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
      toggleRedLED();
    }
    else if (command == "t2") {
      toggleGreenLED();
    }
    else {
      Serial.println("Unknown command: " + command);
    }
  }
  // Process delay commands (D followed by milliseconds)
  else if (command.length() > 2 && command.charAt(0) == 'D') {
    processDelayCommand(command);
  }
  else {
    Serial.println("Invalid command format: " + command);
  }
}

// ===== LED CONTROL FUNCTIONS =====

void turnRedLEDOn() {
  digitalWrite(RED_LED_PIN, HIGH);
  red_led_state = true;
  Serial.println("Red LED: ON");
}

void turnRedLEDOff() {
  digitalWrite(RED_LED_PIN, LOW);
  red_led_state = false;
  Serial.println("Red LED: OFF");
}

void turnGreenLEDOn() {
  digitalWrite(GREEN_LED_PIN, HIGH);
  green_led_state = true;
  Serial.println("Green LED: ON");
}

void turnGreenLEDOff() {
  digitalWrite(GREEN_LED_PIN, LOW);
  green_led_state = false;
  Serial.println("Green LED: OFF");
}

void turnBothLEDsOn() {
  digitalWrite(RED_LED_PIN, HIGH);
  digitalWrite(GREEN_LED_PIN, HIGH);
  red_led_state = true;
  green_led_state = true;
  Serial.println("Both LEDs: ON");
}

void turnBothLEDsOff() {
  digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(GREEN_LED_PIN, LOW);
  red_led_state = false;
  green_led_state = false;
  Serial.println("Both LEDs: OFF");
}

void toggleRedLED() {
  if (red_led_state) {
    turnRedLEDOff();
  } else {
    turnRedLEDOn();
  }
}

void toggleGreenLED() {
  if (green_led_state) {
    turnGreenLEDOff();
  } else {
    turnGreenLEDOn();
  }
}

// ===== DELAY COMMAND PROCESSING =====
void processDelayCommand(String command) {
  // Extract the delay time (everything after 'D')
  String delayStr = command.substring(1);
  
  // Convert to integer (milliseconds)
  int delayMs = delayStr.toInt();
  
  if (delayMs > 0) {
    Serial.print("Delay: ");
    Serial.print(delayMs);
    Serial.println(" ms");
    delay(delayMs);
  } else {
    Serial.println("Invalid delay value: " + delayStr);
  }
}

// ===== STATUS REPORTING =====
void sendStatusReport() {
  Serial.println("=== STATUS REPORT ===");
  Serial.print("Red LED: ");
  Serial.println(red_led_state ? "ON" : "OFF");
  Serial.print("Green LED: ");
  Serial.println(green_led_state ? "ON" : "OFF");
  Serial.println("===================");
} 