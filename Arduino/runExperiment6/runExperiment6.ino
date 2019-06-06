String inputString ="";
String currString ="";
bool stringComplete = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(8, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  digitalWrite(10, LOW);
  digitalWrite(9, LOW);
  digitalWrite(8, HIGH);
  digitalWrite(7, HIGH);
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
  if (currString=="pup\n"){
    digitalWrite(11, HIGH);
    delay(1000);
    digitalWrite(10,HIGH);
  }
  //Serial.println(digitalRead(8));
  if (currString == "up\n"){
    digitalWrite(11, HIGH);  
  } else {
    if (currString!="pup\n") digitalWrite(11, LOW);
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
  if ((currString == "gat\n") /*|| currString == "pmp\n"*/) {
    digitalWrite(9, HIGH);
  } else {
    digitalWrite(9, LOW);
  }
  if (currString == "pmp\n"){
     digitalWrite(10, HIGH);
  } else {
    if (currString != "pup\n") digitalWrite(10,LOW);
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
