/*** LED and Fan Control System ***/
/*
 * This Arduino sketch controls an RGB LED and a fan based on serial commands.
 * It communicates with a Python agent that sends commands via the serial port.
 * 
 * Hardware Connections:
 * - Red LED connected to pin 9
 * - Green LED connected to pin 10
 * - Blue LED connected to pin 11
 * - Fan connected to pin 13
 * - Thermistor connected to pin A5
 * 
 * Communication Protocol:
 * - R: Turn Red LED ON
 * - r: Turn Red LED OFF
 * - G: Turn Green LED ON
 * - g: Turn Green LED OFF
 * - B: Turn Blue LED ON
 * - b: Turn Blue LED OFF
 * - W: Turn all RGB LEDs ON (White)
 * - w: Turn all RGB LEDs OFF
 * - F: Turn Fan ON
 * - f: Turn Fan OFF
 * - S: Send status report
 * 
 * Author: Trylen
 * Date: 2025-04-08
 */

// ===== PIN DEFINITIONS =====
const int RED_PIN = 9;      // Digital pin for Red LED
const int GREEN_PIN = 10;   // Digital pin for Green LED
const int BLUE_PIN = 11;    // Digital pin for Blue LED
const int FAN_PIN = 13;     // Digital pin for Fan
const int THERM_PIN = A5;   // Analog pin for thermistor

// ===== DEVICE STATE TRACKING =====
bool redState = false;      // Track Red LED state (true = ON, false = OFF)
bool greenState = false;    // Track Green LED state (true = ON, false = OFF)
bool blueState = false;     // Track Blue LED state (true = ON, false = OFF)
bool fanState = false;      // Track Fan state (true = ON, false = OFF)
float temperature = 0.0;    // Track temperature reading

// ===== SERIAL COMMUNICATION =====
char inputBuffer[10];       // Buffer for storing incoming serial data
int bufferIndex = 0;        // Index for the input buffer

// ===== SETUP FUNCTION =====
void setup() {
  // Initialize serial communication at 9600 baud rate
  Serial.begin(9600);
  delay(500);  // Allow time for serial connection to establish
  
  // Configure pins as outputs
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  
  // Initialize devices to OFF state
  digitalWrite(RED_PIN, LOW);
  digitalWrite(GREEN_PIN, LOW);
  digitalWrite(BLUE_PIN, LOW);
  digitalWrite(FAN_PIN, LOW);
  
  // Print welcome message and available commands
  Serial.println("\n=== RGB LED and Fan Control System ===");
  Serial.println("System initialized and ready for commands.");
  Serial.println("Available commands:");
  Serial.println("  R - Turn Red LED ON");
  Serial.println("  r - Turn Red LED OFF");
  Serial.println("  G - Turn Green LED ON");
  Serial.println("  g - Turn Green LED OFF");
  Serial.println("  B - Turn Blue LED ON");
  Serial.println("  b - Turn Blue LED OFF");
  Serial.println("  W - Turn all RGB LEDs ON (White)");
  Serial.println("  w - Turn all RGB LEDs OFF");
  Serial.println("  F - Turn Fan ON");
  Serial.println("  f - Turn Fan OFF");
  Serial.println("  S - Send status report");
  Serial.println("===================================\n");
}

// ===== MAIN LOOP =====
void loop() {
  // Read temperature from thermistor
  int rawTemp = analogRead(THERM_PIN);
  temperature = map(rawTemp, 0, 1023, 0, 100) / 10.0; // Simple mapping, adjust as needed
  
  // Check if data is available to read from serial port
  while (Serial.available() > 0) {
    // Read the incoming byte and convert to char
    char inChar = (char)Serial.read();
    
    // Debug print to show received character
    Serial.print("Received command: ");
    Serial.println(inChar);
    
    // Process the command immediately
    processCommand(inChar);
  }
  
  // Small delay to prevent overwhelming the serial buffer
  delay(10);
}

// ===== COMMAND PROCESSING =====
void processCommand(char command) {
  // Process the command based on the received character
  switch (command) {
    case 'R':  // Turn Red LED ON
      Serial.println("Processing command: Turn Red LED ON");
      digitalWrite(RED_PIN, HIGH);
      redState = true;
      Serial.println("Red LED turned ON");
      break;
      
    case 'r':  // Turn Red LED OFF
      Serial.println("Processing command: Turn Red LED OFF");
      digitalWrite(RED_PIN, LOW);
      redState = false;
      Serial.println("Red LED turned OFF");
      break;
      
    case 'G':  // Turn Green LED ON
      Serial.println("Processing command: Turn Green LED ON");
      digitalWrite(GREEN_PIN, HIGH);
      greenState = true;
      Serial.println("Green LED turned ON");
      break;
      
    case 'g':  // Turn Green LED OFF
      Serial.println("Processing command: Turn Green LED OFF");
      digitalWrite(GREEN_PIN, LOW);
      greenState = false;
      Serial.println("Green LED turned OFF");
      break;
      
    case 'B':  // Turn Blue LED ON
      Serial.println("Processing command: Turn Blue LED ON");
      digitalWrite(BLUE_PIN, HIGH);
      blueState = true;
      Serial.println("Blue LED turned ON");
      break;
      
    case 'b':  // Turn Blue LED OFF
      Serial.println("Processing command: Turn Blue LED OFF");
      digitalWrite(BLUE_PIN, LOW);
      blueState = false;
      Serial.println("Blue LED turned OFF");
      break;
      
    case 'W':  // Turn all RGB LEDs ON (White)
      Serial.println("Processing command: Turn all RGB LEDs ON (White)");
      digitalWrite(RED_PIN, HIGH);
      digitalWrite(GREEN_PIN, HIGH);
      digitalWrite(BLUE_PIN, HIGH);
      redState = true;
      greenState = true;
      blueState = true;
      Serial.println("All RGB LEDs turned ON (White)");
      break;
      
    case 'w':  // Turn all RGB LEDs OFF
      Serial.println("Processing command: Turn all RGB LEDs OFF");
      digitalWrite(RED_PIN, LOW);
      digitalWrite(GREEN_PIN, LOW);
      digitalWrite(BLUE_PIN, LOW);
      redState = false;
      greenState = false;
      blueState = false;
      Serial.println("All RGB LEDs turned OFF");
      break;
      
    case 'F':  // Turn Fan ON
      Serial.println("Processing command: Turn Fan ON");
      digitalWrite(FAN_PIN, HIGH);
      fanState = true;
      Serial.println("Fan turned ON");
      break;
      
    case 'f':  // Turn Fan OFF
      Serial.println("Processing command: Turn Fan OFF");
      digitalWrite(FAN_PIN, LOW);
      fanState = false;
      Serial.println("Fan turned OFF");
      break;
      
    case 'S':  // Send status report
      Serial.println("Processing command: Send status report");
      sendStatusReport();
      break;
      
    case '\n':  // Ignore newlines
    case '\r':  // Ignore carriage returns
      break;
      
    default:  // Unknown command
      Serial.print("Unknown command: ");
      Serial.println(command);
      break;
  }
}

// ===== STATUS REPORTING =====
void sendStatusReport() {
  // Print a formatted status report
  Serial.println("\n=== STATUS REPORT ===");
  Serial.print("Red LED: ");
  Serial.println(redState ? "ON" : "OFF");
  Serial.print("Green LED: ");
  Serial.println(greenState ? "ON" : "OFF");
  Serial.print("Blue LED: ");
  Serial.println(blueState ? "ON" : "OFF");
  Serial.print("Fan: ");
  Serial.println(fanState ? "ON" : "OFF");
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");
  Serial.println("====================\n");
} 