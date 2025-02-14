const int THERMISTOR_PIN = A5;    // Analog pin for thermistor
const int SAMPLES = 10;           // Number of samples to average
const int SAMPLE_DELAY = 100;     // Delay between samples in ms
const int READING_DELAY = 1000;   // Delay between readings in ms

void setup() {
  Serial.begin(9600);
  Serial.println("Thermistor Reading Starting...");
  Serial.println("Analog Value (0-1023)");
}

void loop() {
  // Take multiple samples and average them
  long sum = 0;
  for(int i = 0; i < SAMPLES; i++) {
    sum += analogRead(THERMISTOR_PIN);
    delay(SAMPLE_DELAY);
  }
  int avgValue = sum / SAMPLES;
  
  // Print the averaged reading
  Serial.println(avgValue);
  
  delay(READING_DELAY);
} 