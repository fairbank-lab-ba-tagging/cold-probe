String inputString ="";
String currString ="";
bool stringComplete = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(8, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  digitalWrite(7, HIGH);
  digitalWrite(8, HIGH);
  Serial.begin(9600);
  inputString.reserve(200);
  currString.reserve(200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (stringComplete) {
    currString = inputString;
    Serial.println(currString);
    inputString = "";
    stringComplete = false;
  }
  if (currString == "up\n" && digitalRead(8) == 1){
    digitalWrite(11, HIGH);  
  } else {
    digitalWrite(11, LOW);
  }
  if (currString == "dn\n" && digitalRead(7) == 1){
    digitalWrite(12, HIGH);
  } else {
    digitalWrite(12, LOW);
  }
  if (currString == "rtp\n") {
    digitalWrite(8, LOW);
    delay(1000);
    digitalWrite(8, HIGH);
  }
 // Serial.println(digitalRead(7));
}

void serialEvent() {

 while(Serial.available()) {
   char inChar = (char)Serial.read();
   inputString += inChar;
   if (inChar == '\n') {
    stringComplete = true;
   }
  }
}
