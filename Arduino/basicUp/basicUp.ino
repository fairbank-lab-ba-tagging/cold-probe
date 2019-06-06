void setup() {
  // put your setup code here, to run once:
  pinMode(12, OUTPUT);
  pinMode(8, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(12, HIGH);
  Serial.println(digitalRead(8));

  
}
