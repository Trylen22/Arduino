//  TRYLEN STEPHENS - ENGR-120 - CANISTER OVEN PROJECT

//INTEGERS

int tempA;
float tempC;
float tempF;         // Declared but not used, left as is
float setpointC = 25.8;
int setpointA;
int sigma = 2; 
int rled = 9;
int gled = 10;
int bled = 11;
int heater = 7;
int fan = 3; 
int heaterval;
int fanval; 
int Stdev = 3;
STANDARD DEVIATION
//** PIN SETUP**//
void setup() {
  Serial.begin(9600);
  
  pinMode(rled, OUTPUT); // RGB outputs
  pinMode(gled, OUTPUT); //optional
  pinMode(bled, OUTPUT);
  pinMode(heater, OUTPUT);
  pinMode(6, INPUT);
  pinMode(fan, OUTPUT);

  //** CALCULATIONS**//
  setpointA = 12.2727 * setpointC + 231.136;
  int UCLA = setpointA + 3 * sigma;
  int LCLA = setpointA - 3 * sigma;
  float UCLC = 0.0815 * UCLA - 18.833; // Not used further, but retained
  float LCLC = 0.0815* LCLA - 18.833; // Not used further, but retained

  tempC = 0.0815 * tempA - 18.833;
  Serial.println("    ");
  Serial.println("    ");
  Serial.println("    ");
  Serial.print(UCLC);
  Serial.println("   ");
  Serial.print(LCLC);
  Serial.println("   ");
}

void loop() {
  int UCLA = setpointA + 3 * sigma;
  int LCLA = setpointA - 3 * sigma;

  //** PRINT VALUES**//
  String titles[7] = {"LCLA", "SP", "UCLA", "TempA", "TempC", "Heater", "Fan" };
  for (int i = 0; i < 7; i++) {
    Serial.print(titles[i]);
    if (i < 6) {
      Serial.print("    ");
    }
  }
  Serial.println("");

  Serial.print(LCLA); 
  Serial.print("    "); 
  Serial.print(setpointA); 
  Serial.print("     "); 
  Serial.print(UCLA); 
  Serial.print("     "); 
  Serial.print(tempA); 
  Serial.print("      "); 
  Serial.print(tempC); 
  Serial.print("     "); 
  Serial.print(heaterval); 
  Serial.print("         "); 
  Serial.print(fanval); 
  Serial.println("   ");

  if (digitalRead(6)) {
    heaterval = 1;
  }
  if (!digitalRead(6)) {
    heaterval = 0;
  }
  if (digitalRead(fan)) {
    fanval = 1;
  }
  if (!digitalRead(fan)) {
    fanval = 0; 
  }

  //** CALCULATE **//
  tempA = analogRead(5);
  tempC = 0.0944 * tempA - 22.989;
  // tempF = (9.0 / 5.0) * tempC + 32; // Declared, but never used, left as is

  // Mapping color values to temp
  int Redmap = map(tempA, LCLA, UCLA, 0, 200);
  int Bluemap = map(tempA, UCLA, LCLA, 255, 100);
  //int Gmap = map(tempA, UCLA, LCLA, 255, 100);
  //int Gmap = map(tempA, UCLA, LCLA, 0, 100);

  analogWrite(rled, Redmap);
  analogWrite(bled, Bluemap);

  //** CONTROLS**//
  if (tempA > UCLA) {
    FanOn();
    HeaterOff();
    analogWrite(rled, 255);
  }
  if (tempA < setpointA) {
    FanOff();
  }
  if (tempA < LCLA) {
    HeaterOn();
    analogWrite(bled, 255);
  }
  if (tempA = LCLA) {
    FanOff();
  }
  delay(1000);
}

//** USER FUNCTIONS**//
void FanOn() {
  digitalWrite(fan, HIGH);
}

void FanOff() {
  digitalWrite(fan, LOW);
}

void HeaterOn() {
  digitalWrite(heater, HIGH);
}

void HeaterOff() {
  digitalWrite(heater, LOW);
}
