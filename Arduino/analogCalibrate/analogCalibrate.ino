void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int pin = analogRead(0);
  float vlts = pin*5.2/1024;
  Serial.println(vlts);
  delay(100);
}
