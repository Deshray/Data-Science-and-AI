void setup() {
  // put your setup code here, to run once:
pinMode(34, INPUT);
pinMode(13, OUTPUT);
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
int a = analogRead(34);
Serial.println(a);
if (a<2000){
  digitalWrite(13,HIGH);
}
else{
  digitalWrite(13, LOW);
}
}
