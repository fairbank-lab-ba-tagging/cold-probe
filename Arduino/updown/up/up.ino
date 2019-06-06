// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as an output.
  int up = 11;
  int dn = 12;
  pinMode(up, OUTPUT);
  pinMode(dn, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  int up = 11;
  int dn = 12;
  delay(10000);
  digitalWrite(up, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(30000);              // wait for a second
  digitalWrite(up, LOW);    // turn the LED off by making the voltage LOW
}
