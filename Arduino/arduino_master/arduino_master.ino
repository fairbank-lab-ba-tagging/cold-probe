/* Trey Wager & Adam Craycraft
    A simple program to run on the arduino to control the liquid nitrogen
    level and report the pressure from the barometer.
*/

#include <LiquidCrystal.h>

// Setup the lcd display
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Prepare some variables
float pressure;
float power;
bool n2Pump = false;
const int valve = 9;                                // gate valve in runExperiment1
const long fillTime = 1 * 60 * 1000L ;              // 1 min Make sure to cast to long
const long waitTime = 75 * 60 * 1000L;              // 75 min Make sure to cast to long
unsigned long currentMilliseconds = waitTime;
unsigned long lastMilliseconds = 0;

float readBarometer() { // Called to read the barometer
  float agg = 0;
  for (int i = 0; i < 250; i++){ // Average 250 measurementprint time till refill
  String ln2_info;
  lcd.setCursor(5, 1);
  lcd.print("LN2:");
    if (n2Pump) {
      int timeSec = fillTime/1000 - (millis() - lastMilliseconds)/(1000);
      if (timeSec >= 10){
        ln2_info = "fill " + String(timeSec);
      }
      else{
        ln2_info = "fill 0" + String(timeSec);
      }
    }
    else{
      int refillTime = waitTime/(60*1000L) - (currentMilliseconds - lastMilliseconds)/(1000L*60);
      if (refillTime >= 10){
        ln2_info = "wait " + String(refillTime);
      }
      else{
        ln2_info = "wait 0" + String(refillTime);
      }
    }
  lcd.print(ln2_info);
    agg += analogRead(A0);
    delay(1);
  }
  float avg = agg/250;
  return avg * 1.04 - 24;
}

float readPower(){
  float agg = 0;
  for (int i = 0; i < 250; i++){ // Average 250 measurements
    agg += analogRead(A2);
    delay(1);
  }
  float avg = agg/250;
  Serial.println(avg);
  return avg * 10.0 * 5.0 / 1024.0;
}

void display(){
  // Print the pressure
  lcd.clear();
  lcd.print(pressure);
  lcd.setCursor(0,1);
  lcd.print("torr");

  // Print power
  lcd.setCursor(8, 0);
  lcd.print("POW ");
  lcd.print(power);

  // print time till refill
  String ln2_info;
  lcd.setCursor(5, 1);
  lcd.print("LN2:");
    if (n2Pump) {
      int timeSec = fillTime/1000 - (millis() - lastMilliseconds)/(1000);
      if (timeSec >= 10){
        ln2_info = "fill " + String(timeSec);
      }
      else{
        ln2_info = "fill 0" + String(timeSec);
      }
    }
    else{
      int refillTime = waitTime/(60*1000L) - (currentMilliseconds - lastMilliseconds)/(1000L*60);
      if (refillTime >= 10){
        ln2_info = "wait " + String(refillTime);
      }
      else{
        ln2_info = "wait 0" + String(refillTime);
      }
    }
  lcd.print(ln2_info);
}

void setup() {
  pinMode(valve, OUTPUT);
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.print("BEGIN!");
  delay(1000);
}

void loop() {
  currentMilliseconds = millis();

  if (currentMilliseconds - lastMilliseconds >= waitTime) {
    digitalWrite(valve, HIGH);
    lastMilliseconds = millis();
    n2Pump = true;
  }
  else if (currentMilliseconds - lastMilliseconds < fillTime){
    digitalWrite(valve, HIGH);
    n2Pump = true;
  }
  else{
    digitalWrite(valve, LOW);
    n2Pump = false;
  }

  power = readPower();

  pressure = readBarometer();

  display();
}
