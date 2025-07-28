/*** TRYLEN STEPHENS ENGR-121-HW 6***


// Define pin connections
const int THERM_PIN = A5;    // Analog pin for thermistor
const int RED_PIN   = 8;     // Digital pin for Red LED (heater on indicator)
const int GREEN_PIN = 10;    // Digital pin for Green LED (heater off indicator)
const int BLUE_PIN  = 11;
const int FAN = 13 ;   // Digital pin for Blue LED (unused in this example)


//-----------------------------------------------------------------------------


// Setpoint and control parameters
const float setPointTemp = 23.2; 
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
  
  
  Serial.print("Analog Reading: ");
  Serial.print(TempA);
  Serial.print(" | Temperature: ");
  Serial.print(TempC, 3);
  Serial.print("  C | ");
  Serial.print(temperatureF, 3);
  Serial.println("  F");
  
 
  if (TempC > UCLC) {
    Heateron();
    Serial.println("Status: Temperature is above UCL.");
  }
  else if (TempC < LCLC) {
    Heateroff();
    Serial.println("Status: Temperature is below LCL.");
  }
  else {
    
    Serial.println("Status: Temperature is within control limits.");
  }
  
  Serial.println("------------------------------");
  delay(5000); 
}


//----------------------------------------------------------------------



void Heateron(){
  
  digitalWrite(FAN, HIGH);
  Serial.println("Fan is ON.");
  digitalWrite(RED_PIN,HIGH);
}

void Heateroff(){
  
  digitalWrite(FAN, LOW);
  Serial.println("Fan is OFF.");
}
