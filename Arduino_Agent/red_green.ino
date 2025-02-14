const int GREEN_LED = 11;
const int RED_LED = 13;

void setup() {
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  Serial.begin(9600);  // Start serial communication
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    switch(command) {
      case 'G':  // Green ON
        digitalWrite(GREEN_LED, HIGH);
        break;
      case 'g':  // Green OFF
        digitalWrite(GREEN_LED, LOW);
        break;
      case 'R':  // Red ON
        digitalWrite(RED_LED, HIGH);
        break;
      case 'r':  // Red OFF
        digitalWrite(RED_LED, LOW);
        break;
      case 'B':  // Both ON
        digitalWrite(GREEN_LED, HIGH);
        digitalWrite(RED_LED, HIGH);
        break;
      case 'b':  // Both OFF
        digitalWrite(GREEN_LED, LOW);
        digitalWrite(RED_LED, LOW);
        break;
    }
  }
} 