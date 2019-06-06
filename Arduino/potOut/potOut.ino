int pot = 5;
float val = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void takeReading(){
  int i = 0;
  float agg = 0.0;
  while(i<100){
  agg = agg + analogRead(5);
  i = i + 1;
  delay(5);
  }
  val = agg/(i+1);
  Serial.println(val);
}

void loop() {
  // put your main code here, to run repeatedly:
  takeReading();
  delay(1000); 
}
