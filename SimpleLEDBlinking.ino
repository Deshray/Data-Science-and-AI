int LED1 = 13;
int LED2 = 12;
int LED3 = 14;
int ldr = 34;

void setup() {
  pinMode(LED1,OUTPUT);
  pinMode(LED2,OUTPUT);
  pinMode(LED3,OUTPUT);
  pinMode(ldr,INPUT);
  Serial.begin(9600);
}

void loop() {
  Serial.println(analogRead(ldr));

  if (analogRead(ldr)>= 3000){
    Serial.print("LED is 255,0,0 :");
    setColor(0,0,255);
  }
  else if(analogRead(ldr)>= 2000){
    setColor(0,255,0);
    Serial.print("LED is 0,255,0 :");
  }
  else if(analogRead(ldr)>= 1000){
    setColor(255,0,0);
    Serial.print("LED is 0,0,255 :");
  }
  else {
    setColor(0,0,0);
    Serial.print("LED is 0,0,0 :");
  }
  delay(20);
}


void setColor(int red, int green, int blue)
{
  // #ifdef COMMON_ANODE
  // red = 255 - red;
  // green = 255 - green;
  // blue = 255 - blue;
  // #endif
  analogWrite(LED1, red);
  analogWrite(LED2, green);
  analogWrite(LED3, blue);
}