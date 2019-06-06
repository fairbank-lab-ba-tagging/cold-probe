
const  int dn = 12;      //down output when this pin is high motor lowers probe
const  int up = 11;      //up output when this pin is high motor raises probe
const  int gat = 10;     //gate valve output when this pin is high gate valve will close
const  int pmp = 9;      //pump valve output when this pin is high pump valve will open 
const  int top = 8;      //top sensor input when this pin is high motor stops
const  int bot = 7;      //bottom sensor input when this pin is high motor stops
const  int gdn = 6;      //down toggle input when this pin is high motor can go down and not up
const  int gup = 5;      //up toggle input when this pin is high motor can go up and not down 
const  int cgt = 4;      //close gate toggle when this pin is high gate valve can close
const  int opm = 3;      //open pump toggle when this pin is high pump out valve can open
const  int rdg = 2;


void setup() {
  

  pinMode(dn,OUTPUT);
  pinMode(up,OUTPUT);
  pinMode(gat,OUTPUT);
  pinMode(pmp,OUTPUT);
  pinMode(top,INPUT_PULLUP);
  pinMode(bot,INPUT_PULLUP);
  pinMode(gdn,INPUT_PULLUP);
  pinMode(gup,INPUT_PULLUP);
  pinMode(cgt,INPUT_PULLUP);
  pinMode(opm,INPUT_PULLUP);
  pinMode(rdg,INPUT_PULLUP);
  digitalWrite(dn, LOW);
  digitalWrite(up, LOW);
  digitalWrite(gat, LOW);
  digitalWrite(pmp, LOW);
  digitalWrite(top, HIGH);
  digitalWrite(bot, HIGH);
  digitalWrite(gdn, HIGH);
  digitalWrite(gup, HIGH);
  digitalWrite(cgt, HIGH);
  digitalWrite(opm, HIGH);
  digitalWrite(rdg, HIGH);
  Serial.begin(9600);

}

void loop() {

  //This finds the probe and decides if you want it moving
  bool isTop = digitalRead(top) == LOW; //is it at the top
  bool isBot = digitalRead(bot) == LOW; //is it at the bottom
  bool isBtw = !(isTop || isBot);//is it between the top and bottom
  bool wantDn = digitalRead(gdn) == LOW;   //do I want probe to go down
  bool wantUp = digitalRead(gup) == LOW;   //do I want probe to go up
  bool wantMvg = (wantDn || wantMvg);       //do I want the probe moving at all
  
  //This stops movement if probe has reached a limit
  if(!isBtw || !wantMvg){
    digitalWrite(up, LOW);
    digitalWrite(dn, LOW);
  } 

 // bool testSwitch = digitalRead(rdg) == LOW;
 // Serial.println(testSwitch);

  //This gets the toggle positions, valve states, and 
  bool wantGtC = digitalRead(cgt) == LOW;  //do I want gate valve to close
  bool wantPmpO = digitalRead(opm) == LOW; //do I want pumo out valve to open
  bool GtC = digitalRead(gat) == HIGH;      //is gate valve closed
  bool PmpO = digitalRead(pmp) == HIGH;     //is pump valve open
  bool isUp = digitalRead(up) == HIGH;      //is motor going up
  bool isDn = digitalRead(dn) == HIGH;      //is motor going down
  
  //This takes care of toggle edge cases:
  //Leave pump valve closed if gate valve is open
  /*if(!GtC){
    wantPmpO = false;
  }*/
  //Kill motor if both up and down are toggled
  if(wantDn && wantUp){
    wantUp = false;
    digitalWrite(up, LOW);
    wantDn = false;
    digitalWrite(dn, LOW);
  }
  
  //This does the desired things
  //Go up
  if(wantUp/* && isBtw*/){ 
    digitalWrite(up, HIGH);
    Serial.println("want up");
  }
  //Go down
  if(wantDn/* && isBtw*/){
    digitalWrite(dn, HIGH);
    Serial.println("want down");
  }
  //Open or close pump out
  /*if(wantPmpO /*&& GtC){
    digitalWrite(pmp, HIGH);
  }
  else{
    digitalWrite(pmp, LOW);
  }
  //Close or open gate
  if (wantGtC /*&& isUp){
    digitalWrite(gat, HIGH);
  }
  else{
    digitalWrite(gat, LOW);
  }*/
  //Close gate then open PO
  if (wantGtC){
    digitalWrite(gat, HIGH);
    delay(3000);
    if (wantPmpO){
      digitalWrite(pmp, HIGH);
    }
  }
  else{
    digitalWrite(gat, LOW);
    digitalWrite(pmp, LOW);
  }
  
}
