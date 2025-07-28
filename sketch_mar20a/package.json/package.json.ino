//*** TRYLEN STEPHENS ENGR-121-***


// Define pin connections
const int THERM_PIN = A5;    // Analog pin for thermistor
const int RED_PIN   = 9;     // Digital pin for Red LED (heater on indicator)
const int GREEN_PIN = 10;    // Digital pin for Green LED (heater off indicator)
const int BLUE_PIN  = 11;
const int FAN = 3 ;
const int HEATER = 13;   // Digital pin for Blue LED 


//-----------------------------------------------------------------------------


// Setpoint and control parameters
const float setPointTemp = 24.0; 
int SetpointA;                    
float TempC;                      
int TempA;                        
float UCLA, LCLA;                 
float UCLC, LCLC;                 
const int STD_DEV = 3;            
const int lim = 3;   

//-----------------------------------------------------------------------------

void setup() {
  Serial.begin(9600);
  delay(500);
  
  // Calculate setpoint in analog
  SetpointA = 11.9673 * setPointTemp + 261.7856;
  
  // Calculate the Analog C.L
  UCLA = SetpointA + (lim * STD_DEV);
  LCLA = SetpointA - (lim * STD_DEV);
  
  // Convert control limits from analog to C
  UCLC = (0.0816 * UCLA) - 20.8683;
  LCLC = (0.0816 * LCLA) - 20.8683;
  
  // Print setup information
  Serial.println("\n=== TEMPERATURE CONTROL SYSTEM SETUP ===");
  Serial.println(" ");
  Serial.print("Setpoint Temperature: ");
  Serial.print(setPointTemp);
  Serial.println(" C");
  Serial.print("Setpoint Analog Value: ");
  Serial.println(SetpointA);
  
  Serial.print("Lower Control Limit (Analog): ");
  Serial.println(LCLA);
  Serial.print("Upper Control Limit (Analog): ");
  Serial.println(UCLA);
  
  Serial.print("Lower Control Limit (C): ");
  Serial.println(LCLC);
  Serial.print("Upper Control Limit (C): ");
  Serial.println(UCLC);
  Serial.println(" ");
  Serial.println("=========================================\n");
  
  
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(FAN, OUTPUT);
  pinMode(HEATER, OUTPUT);
  
  
  digitalWrite(RED_PIN, LOW);
  digitalWrite(GREEN_PIN, LOW);
  digitalWrite(BLUE_PIN, LOW);
}


//----------------------------------------------------------------------


void loop() {
  
  TempA = analogRead(THERM_PIN);
  // Convert analog reading to C
  TempC = 0.0816 * TempA - 20.8683;
  // Convert C to F
  float temperatureF = (9.0 / 5.0) * TempC + 32.0;
  
  // Mapping color values to temperature
  int Redmap = map(TempA, LCLA, UCLA, 0, 200);
  int Bluemap = map(TempA, UCLA, LCLA, 255, 100);
  
  analogWrite(RED_PIN, Redmap);
  analogWrite(BLUE_PIN, Bluemap);
  
  Serial.print("Analog Reading: ");
  Serial.print(TempA);
  Serial.print(" | SPA: ");
  Serial.print(SetpointA);
  Serial.print(" | LCLA: ");
  Serial.print(LCLA);
  Serial.print(" | UCLA: ");
  Serial.print(UCLA);
  Serial.print(" | Temperature: ");
  Serial.print(TempC, 3);
  Serial.print("  C | ");
  Serial.print(temperatureF, 3);
  Serial.println("  F");
  
   if (TempA < LCLA) {
    HeaterON();
    FanOFF();
    Serial.println("Heater is on");
  }
  // 2. Between LCLA and UCLA
  else if (TempA >= LCLA && TempA <= UCLA) {
    // If heater is already ON, keep it ON
    if (digitalRead(HEATER) == HIGH) {
      HeaterON();
      FanOFF();
    }
    // Otherwise, if fan is ON, keep fan ON until reaching setpoint
    else if (digitalRead(FAN) == HIGH) {
      if (TempA <= SetpointA) {
        FanOFF();
        HeaterOFF();
      } else {
        FanON();
        HeaterOFF();
      }
    }
    else {
      // In deadband, no change if nothing is running
      HeaterOFF();
      FanOFF();
    }
  }
  // 3. Above UCLA: heater OFF, fan ON
  else if (TempA > UCLA) {
    HeaterOFF();
    FanON();
  }
  
  Serial.println("---------------------------------------------------------");
  delay(1000);
}


//----------------------------------------------------------------------



void FanON(){
  
  digitalWrite(FAN, HIGH);
  Serial.println("Fan is ON.");
  
}

void FanOFF(){
  
  digitalWrite(FAN, LOW);
  Serial.println("Fan is OFF.");
  
}

void HeaterON(){
  digitalWrite(HEATER, HIGH);
  Serial.println("Heater is ON");
}

void HeaterOFF(){
  digitalWrite(HEATER, LOW);
  Serial.println("Heater is OFF");
}

