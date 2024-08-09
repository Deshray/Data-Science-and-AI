// void setup() {
//   pinMode(32, INPUT);
//   Serial.begin(9600);
// }

// void loop() {
//   int a = digitalRead(32);
//   if (a == 1) {
//     Serial.println("No magnet");
//   }
//   else {
//     Serial.println("Magnet present");
//   }
// }

int x = 0;
int count = 0;
unsigned long start = 0;
unsigned long timeold = 0;
int revolutions = 0;

void setup() {
  pinMode(32, INPUT);
  Serial.begin(9600);
}

void loop() {
  x = magnet_detect(32);
  if(x==0){
    if(revolutions==2){
      Serial.println(calculateRPM());
    }
  }
}
long calculateRPM() {
  long rpm = (60000/(millis() - timeold));
  timeold = millis();
  revolutions = 0;
  return rpm;
}
int magnet_detect(int pin){
  int a = digitalRead(pin);
  if (a == 1) {
  }
  else {
    revolutions = revolutions + 1;
    Serial.println("Magnet present");
    while(digitalRead(32)==0){

    }
    if(revolutions == 1){
      timeold = millis();
    }
    Serial.println(millis());
  }
  return a;
}