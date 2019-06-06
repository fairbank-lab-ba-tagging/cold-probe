/* Trey Wager & Adam Craycraft

    A simple program to run on the arduino to control the liquid nitrogen
    level and report the pressure from the barometer.
*/

#include <LiquidCrystal.h>

// Setup the lcd display
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Prepare some variables
const int valve = 9;                                // gate valve in runExperiment1
const long fillTime = 1 * 60 * 1000L ;                  // 1 min Make sure to cast to long
const long waitTime = 75 * 60 * 1000L;              // 75 min Make sure to cast to long
unsigned long currentMilliseconds = waitTime;
unsigned long lastMilliseconds = 0;

void fill() { // Called to refill the nitrogen
  lcd.clear();
  lcd.print("FILLING NITROGEN");

  digitalWrite(valve, HIGH);
  lastMilliseconds = millis();

  while (millis() - lastMilliseconds < fillTime) {
    lcd.setCursor(0, 1);
    int timeSec = fillTime/1000 - (millis() - lastMilliseconds)/(1000);
    if (timeSec >= 10){
      lcd.print(timeSec);
    }
    else{
      lcd.print("0");
      lcd.print(timeSec);
    }
    delay(100);
  }
  digitalWrite(valve, LOW);
}

float readBarometer() { // Called to read the barometer
  float agg = 0;
  for (int i = 0; i < 50; i++){ // Average 50 measurements
    agg += analogRead(A0);
    delay(5);
  }
  return agg/50;
}

void displayPressure(float pressure){ // Display the pressure and time till refill
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(pressure);

  lcd.setCursor(0,1);
  lcd.print("torr");

  // time till refill
  int refillTime = waitTime/(60*1000L) - (currentMilliseconds - lastMilliseconds)/(1000L*60);
  lcd.setCursor(14, 1);
    if (refillTime >= 10){
      lcd.print(refillTime);
    }
    else{
      lcd.print("0");
      lcd.print(refillTime);
    }
}

void setup() {
  pinMode(valve, OUTPUT);
  Serial.begin(9600);
  lcd.begin(16, 2);
}

void loop() {
  // This is for controlling the nitrogen valve
  if (currentMilliseconds - lastMilliseconds >= waitTime) {
    fill();
  }
  currentMilliseconds = millis();

  // For reading the barometer
  float pressure = readBarometer() * 1.04 - 24; // linear fit calibration
  displayPressure(pressure);
}
