const int thermistorPin = A5;  // Analog pin connected to the thermistor

void setup() {
  Serial.begin(9600);  // Start serial communication
}

void loop() {
  int analogValue = analogRead(thermistorPin);  // Read the analog value
  
  // Just send the raw analog value
  Serial.println(analogValue);
  
  delay(100);  // Small delay between readings
}