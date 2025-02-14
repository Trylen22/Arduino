// Test pins for RGB LED
const int RED_PIN = 9;    // Red LED pin
const int BLUE_PIN = 10;  // Blue LED pin

// Test values
const int TEST_DELAY = 50;     // Delay between steps (ms)
const int ANALOG_MIN = 398;    // Equivalent to your LCL
const int ANALOG_MAX = 422;    // Equivalent to your UCL
int testValue = ANALOG_MIN;    // Starting value
int stepSize = 1;             // How much to change each step

void setup() {
  // Configure LED pins
  pinMode(RED_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  
  Serial.begin(9600);
  Serial.println("RGB Fade Test Starting...");
  Serial.println("Value,Red,Blue");
}

void loop() {
  // Map test value to LED intensities
  int redIntensity = map(testValue, ANALOG_MIN, ANALOG_MAX, 0, 255);
  int blueIntensity = map(testValue, ANALOG_MIN, ANALOG_MAX, 255, 0);
  
  // Constrain values
  redIntensity = constrain(redIntensity, 0, 255);
  blueIntensity = constrain(blueIntensity, 0, 255);
  
  // Set LED colors
  analogWrite(RED_PIN, redIntensity);
  analogWrite(BLUE_PIN, blueIntensity);
  
  // Print values for debugging
  Serial.print(testValue);
  Serial.print(",");
  Serial.print(redIntensity);
  Serial.print(",");
  Serial.println(blueIntensity);
  
  // Update test value
  testValue += stepSize;
  
  // Reverse direction at limits
  if (testValue >= ANALOG_MAX || testValue <= ANALOG_MIN) {
    stepSize = -stepSize;
  }
  
  delay(TEST_DELAY);
}