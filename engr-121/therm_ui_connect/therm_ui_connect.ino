const int thermistorPin = A5;  // Analog pin connected to the thermistor
const float setpointC = 22.5;  // Setpoint temperature in Celsius
const float UCL = 23.5;        // Upper Control Limit (from analysis)
const float LCL = 21.5;        // Lower Control Limit (from analysis)

// For analog value control limits
const int ANALOG_UCL = 519;    // Upper Control Limit in analog
const int ANALOG_LCL = 495;    // Lower Control Limit in analog

// LED pins
const int red_LED = 9;
const int green_LED = 11;
const int blue_LED = 10;

// Calibration constants
const float TEMP_SLOPE = 0.0815;
const float TEMP_INTERCEPT = -18.8333;

String LED_STATUS = "";

void setup() {
  Serial.begin(9600);
  
  // Configure LED pins
  pinMode(red_LED, OUTPUT);
  pinMode(green_LED, OUTPUT);
  pinMode(blue_LED, OUTPUT);
  
  // Turn off all LEDs initially
  analogWrite(red_LED, 0);
  analogWrite(green_LED, 0);
  analogWrite(blue_LED, 0);
  
  // Print header
  Serial.println("Analog Value, Temp (C), Temp (F), Status");
}

float getTemperature(int analogValue) {
  return (TEMP_SLOPE * analogValue) + TEMP_INTERCEPT;
}

float celsiusToFahrenheit(float celsius) {
  return (celsius * 9.0 / 5.0) + 32.0;
}

void updateLEDs(int analogValue, float temperature) {
  // Clear all LEDs first
  analogWrite(red_LED, 0);
  analogWrite(green_LED, 0);
  analogWrite(blue_LED, 0);
  
  // Use both analog and temperature values for more precise control
  if (analogValue > ANALOG_UCL || temperature > UCL) {
    // Too hot - Red LED
    analogWrite(red_LED, 255);
    LED_STATUS = "HOT";
  } else if (analogValue < ANALOG_LCL || temperature < LCL) {
    // Too cold - Blue LED
    analogWrite(blue_LED, 255);
    LED_STATUS = "COLD";
  } else {
    // Just right - Green LED
    analogWrite(green_LED, 255);
    LED_STATUS = "GOOD";
  }
}

void loop() {
  // Read sensor value
  int analogValue = analogRead(thermistorPin);
  
  // Calculate temperatures
  float tempC = getTemperature(analogValue);
  float tempF = celsiusToFahrenheit(tempC);
  
  // Update LED status based on both analog and temperature values
  updateLEDs(analogValue, tempC);
  
  // Print detailed data to serial
  Serial.print("Raw:");
  Serial.print(analogValue);
  Serial.print(",TC:");
  Serial.print(tempC, 1);
  Serial.print(",TF:");
  Serial.print(tempF, 1);
  Serial.print(",LED:");
  Serial.println(LED_STATUS);
  
  // Wait 5 seconds between readings
  delay(5000);
}