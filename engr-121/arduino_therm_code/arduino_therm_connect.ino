//** INTEGERS**//
int tempA;
float tempC;
float tempF;
float setpointC= 25.1;
int setpointA;
int sigma = 1; 
int rled = 9;
int gled = 10;
int bled = 11;
int heater = 7;
int fan = 3; 
int heaterval; 
int fanval; 

//** I/O SETUP**//
void setup() {
Serial.begin (9600);
pinMode (rled, OUTPUT); //RGB outputs
pinMode (gled, OUTPUT); 
pinMode (bled, OUTPUT);
pinMode(heater, OUTPUT);
pinMode(6, INPUT);
pinMode(fan, INPUT);

//** CALCULATIONS**//
setpointA=10.425*setpointC+247.45;
int UCLA=setpointA+3*sigma;
int LCLA = setpointA-3*sigma;
int UCLC= 0.0944*UCLA-22.989;
int LCLC = 0.0944*LCLA-22.989;
tempC=0.0944*tempA-22.989;
Serial.println("    ");
}



void loop() {
int UCLA=setpointA+3*sigma;
int LCLA = setpointA-3*sigma;

//** PRINT VALUES**//
String titles[7] = {"LCLA", "SP", "UCLA", "TempA", "TempC", "Heater", "Fan"};
for (int i=0; i < 7; i++) {
  Serial.print(titles[i]);
  if (i<6) {
    Serial.print("    ");
  }
}
Serial.println("");
Serial.print(LCLA); Serial.print("    "); Serial.print(setpointA); Serial.print("     "); Serial.print(UCLA); 
Serial.print("     "); Serial.print(tempA); Serial.print("      "); Serial.print(tempC); Serial.print("     ");
Serial.print(heaterval); Serial.print("         "); Serial.print(fanval); Serial.println("   ");


if (digitalRead(6)) {
  heaterval=1;
}
if (!digitalRead(6)){
  heaterval=0;
}
if (digitalRead(fan)){
  fanval=1;
}
if (!digitalRead(fan)){
  fanval=0; 
}

//** CALCULATE CRITERIA**//
tempA = analogRead(5);
tempC=0.0944*tempA-22.989;

//tempF=(9/5)*tempC+32;
int Redmap = map (tempA, LCLA, UCLA, 0, 200); //mapping color values to temp
int Bluemap = map (tempA, UCLA, LCLA, 255, 100);
  analogWrite (rled, Redmap);
  analogWrite (bled, Bluemap);

//** CONTROLS**//
   if (tempA > UCLA) {
    FanOn();
    HeaterOff();
    analogWrite (rled, 255); }
   if (tempA < setpointA) {
    FanOff();
   }
   if (tempA< LCLA) {
    HeaterOn();
    analogWrite(bled, 255);
   }

   delay (1500);
}


//** USER FUNCTIONS**//
void FanOn() {
  digitalWrite (fan, HIGH);
}
void FanOff() {
  digitalWrite (fan, LOW);
}

void HeaterOn() {
  digitalWrite(heater, HIGH);
}

void HeaterOff() {
  digitalWrite (heater, LOW);
}
