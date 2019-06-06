void setup() {
  // put your setup code here, to run once:
  int on = 12;
  pinMode(on,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int on = 12;
  delay(1000);
  digitalWrite(on, HIGH);
  delay(2000);
  int val = digitalRead(on);
  Serial.print(val);
  delay(1000);
  digitalWrite(on,HIGH);
  delay(2000);
  digitalWrite(on, LOW);
  val = digitalRead(on);
  Serial.print(val);
  Serial.print("\n");
}
