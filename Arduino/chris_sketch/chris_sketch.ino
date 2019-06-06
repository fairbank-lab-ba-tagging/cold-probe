float val = 0.0;
float last_val = 0.0;
float der = 0;
int iter = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(2,OUTPUT);
  Serial.begin(9600);
  pinMode(3,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(2,LOW);
  //last_val = val;
  val = analogRead(5)*5.0/1024;
  //der = val - last_val;
  //Serial.println(digitalRead(3));
  if(val>2 & digitalRead(3) == HIGH  /*& der>0.0*/) {
    if (iter == 0) 
    {
      iter = 1;
      delay(100);
      return;
    }
    digitalWrite(2,HIGH);
    delay(70);
    digitalWrite(2,LOW);
    delay(250);
  }
  if (digitalRead(3) == LOW & iter == 1) iter = 0;
}
