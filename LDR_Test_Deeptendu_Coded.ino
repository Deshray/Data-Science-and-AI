void setup() {
  // put your setup code here, to run once:
pinMode(32, INPUT);
pinMode(13, OUTPUT);
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int a = analogRead(32);
  Serial.println(a);
  if (a<150){
    digitalWrite(13,HIGH);
    Serial.println("led high");
  }
  else{
    digitalWrite(13,LOW);
    Serial.println("led low");
  }
  delay(500);
}