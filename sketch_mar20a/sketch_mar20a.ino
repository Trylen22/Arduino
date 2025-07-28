
const int THERM_PIN = A5;    // Analog pin for thermistor
const int RED_PIN   = 9;     // Digital pin for Red LED
const int GREEN_PIN = 10;    // Digital pin for Green LED
const int BLUE_PIN  = 11;    // Digital pin for Blue LED


const float setPointTemp = 22.5;  
int SetpointA;
float TempC;
int TempA;
float UCLA, LCLA;
float UCLC, LCLC;
const int STD_DEV = 3;
const int lim = 3;



void setup() {
  Serial.begin(9600);
  delay(500);
  SetpointA = 11.9673*setPointTemp + 261.7856;
  Serial.print(" *** SETPOINT A *** ");Serial.print(SetpointA);
  Serial.print(" *** DEG C *** ");Serial.println(setPointTemp);

  UCLA = SetpointA + (lim * STD_DEV);
  LCLA = SetpointA - (lim * STD_DEV);

 UCLC = (0.0816 * UCLA) + 20.8683;
 LCLC =( 0.0816 * LCLA )-20.8683;

 Serial.println("\n=== TEMPERATURE CONTROL SYSTEM ===");
  Serial.print("Setpoint: ");
  Serial.print(setPointTemp);
  Serial.print("°C (Analog: "); 
  Serial.print(SetpointA); 
  Serial.println(")");
  Serial.print("Standard Deviation: ");
  Serial.println(STD_DEV);
  Serial.print("LCL: "); 
  Serial.print(LCLC); 
  Serial.print("°C (Analog: ");
  Serial.print(LCLA); 
  Serial.println(")");
  Serial.print("UCL: "); 
  Serial.print(UCLC); 
  Serial.print("°C (Analog: ");
   Serial.print(UCLA); Serial.println(")");
  Serial.println("===================================\n");

  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  digitalWrite(RED_PIN, LOW);
  digitalWrite(GREEN_PIN, LOW);
  digitalWrite(BLUE_PIN, LOW);
}

void loop() {
  int TempA = analogRead(THERM_PIN);
  float TempC = 0.0816 * TempA - 20.8683;
  float temperatureF = (9.0 / 5.0) * TempC + 32.0;

 
  Serial.print("analog = ");
  Serial.print(TempA);
  Serial.print(", Temperature = ");
  Serial.print(TempC, 4);
  Serial.print(" degC, Temperature = ");
  Serial.print(temperatureF, 3);
  Serial.println(" degF");

  if (TempC < LCLC) {
    Heateron();}
   else {
    Heateroff();
  
  if(TempC > UCLC){
    Heateroff();
  }
  
  }
  delay(5000);
}





void Heateron(){

  digitalWrite(RED_PIN, HIGH);
  digitalWrite(GREEN_PIN, LOW);
  digitalWrite(BLUE_PIN, LOW);
  Serial.print(" ");
  Serial.println("  HEATER ON  ");
  Serial.println(" ");
}

void Heateroff(){
    digitalWrite(RED_PIN, LOW);
    digitalWrite(GREEN_PIN, HIGH);
    digitalWrite(BLUE_PIN, LOW);
    Serial.print("  ");
    Serial.println("  HEATER OFF  ");
    Serial.println("  ");

}
