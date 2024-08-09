int revolutions = 0;
float rpm = 0;
unsigned long start;
unsigned long current;

void setup() {
  pinMode(32, INPUT);
  Serial.begin(9600);
  start = millis();
}

void loop() {
  current = millis();
  if (digitalRead(32) == 0 && revolutions == 0) { 
    Serial.println("Magnet held");
    while(digitalRead(32)==0){
    }
    start = millis();
    Serial.println("Magnet left");
    revolutions = revolutions + 1;
  } 
  else {
    if(digitalRead(32)==0 && revolutions == 1) {
      Serial.println("Magnet held");
      while(digitalRead(32)==0){
      }
      current = millis();
      Serial.println("Magnet left");
      rpm = revolutions/((current - start)/60000.0);
      start = current;
      revolutions = 0;
      Serial.print("RPM is: ");
      Serial.println(rpm);
    }
    else {
      //Serial.println("Magnet not detected");
    }
  }  
}