
const int valve = 9; //gate valve in runExperiment1
const long fillTime = 4; //in .25 min
const long waitTime = 300; //in .25 min
const long convert = 15000;
unsigned long currentMilliseconds = waitTime*convert;
unsigned long lastMilliseconds = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(valve, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (currentMilliseconds - lastMilliseconds >= waitTime*convert){
    digitalWrite(valve, HIGH);
    lastMilliseconds = millis();
    while(millis()-lastMilliseconds<fillTime*convert){
      delay(1); 
    }
  }
  else{
      digitalWrite(valve, LOW);
    }
    delay(10); 
    currentMilliseconds = millis();
}
