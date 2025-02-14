const int GREEN_LED = 11;
const int RED_LED = 13;

// Variables to track LED states
bool greenState = false;
bool redState = false;

void setup() {
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  Serial.begin(9600);
  
  // Initial state
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(RED_LED, LOW);
  
  // Debug message
  Serial.println("Arduino ready!");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    Serial.print("Received command: ");
    Serial.println(command);
    
    switch(command) {
      case 'G':  // Green ON
        greenState = true;
        Serial.println("Green ON");
        break;
      case 'g':  // Green OFF
        greenState = false;
        Serial.println("Green OFF");
        break;
      case 'R':  // Red ON
        redState = true;
        Serial.println("Red ON");
        break;
      case 'r':  // Red OFF
        redState = false;
        Serial.println("Red OFF");
        break;
      case 'B':  // Both ON
        greenState = true;
        redState = true;
        Serial.println("Both ON");
        break;
      case 'b':  // Both OFF
        greenState = false;
        redState = false;
        Serial.println("Both OFF");
        break;
      default:
        Serial.println("Unknown command");
        break;
    }
    
    // Update LED states
    digitalWrite(GREEN_LED, greenState);
    digitalWrite(RED_LED, redState);
    
    // Debug current states
    Serial.print("Green state: ");
    Serial.print(greenState);
    Serial.print(" Red state: ");
    Serial.println(redState);
  }
}