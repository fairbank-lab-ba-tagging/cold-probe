
int pot = 5;
float val = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  val = analogRead(pot)*5.0/1024;
  Serial.println(val);
  delay(1900); 
}
