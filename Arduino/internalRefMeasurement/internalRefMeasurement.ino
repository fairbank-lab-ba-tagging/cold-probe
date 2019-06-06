const uint8_t pinLED = 13;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("\n\r\n\r");

  pinMode( pinLED, OUTPUT);
  digitalWrite( pinLED, LOW);
  delay(1000);

  analogReference( INTERNAL );
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(analogRead(0));
  digitalWrite(pinLED,HIGH);
  delay(1000);
}
