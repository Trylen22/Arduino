// Define pin numbers
const int GREEN_LED = 11;
const int RED_LED = 13;

void setup() {
  // Set LED pins as outputs
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
}

// Function to turn on green LED
void turnOnGreen() {
  digitalWrite(GREEN_LED, HIGH);
  digitalWrite(RED_LED, LOW);
}

// Function to turn on red LED
void turnOnRed() {
  digitalWrite(RED_LED, HIGH);
  digitalWrite(GREEN_LED, LOW);
}

void loop() {
  // You can test the functions here
  // For example:
  turnOnGreen();
  delay(1000);
  turnOnRed();
  delay(1000);
}