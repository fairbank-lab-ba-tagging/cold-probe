void setup() {
  // put your setup code here, to run once:
  //Start serial connection
  Serial.begin(9600);
  //Configure pins as desired
  pinMode(12, INPUT_PULLUP);
  pinMode(13, OUTPUT);
}

bool isup = false;
bool goup = true;

void loop() {
  // put your main code here, to run repeatedly:
  //read switch pin value
  int sPinVal = digitalRead(2);
  //print result
  
  //change LED
  if (sPinVal == HIGH){
    digitalWrite(13, LOW);
    isup = false;
  } else {
    digitalWrite(13, HIGH);
    isup = true;
  }
  delay(500);
  if (isup == true){
    goup = false;
    Serial.println("It's up");
  } else {
    Serial.println("It's going up");
  }
}
