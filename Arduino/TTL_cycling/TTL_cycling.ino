
const int sig = 9; //gate valve in runExperiment1
const float upT = .1; //in seconds
const float waitT = 1; //in seconds
const float convert = 1000;
float currentT = 0;
float lastT = 0;
//bool on = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(sig, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  //delay(1000);
  currentT = millis();
  
  if ((currentT - lastT) >= (upT*convert)){
    digitalWrite(sig,LOW);
    Serial.println("down");
    //on = false;
  }

  Serial.println(currentT);
  Serial.println(lastT);
  
  if ((currentT - lastT) >= (waitT*convert)){
    digitalWrite(sig,HIGH);
    lastT = currentT;
    //on = true;
    Serial.println("up");
  }
  
}
