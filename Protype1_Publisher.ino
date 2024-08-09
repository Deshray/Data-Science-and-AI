#include <DHT.h>
#include <DHT_U.h>
#include <Wire.h>

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include <WiFi.h>
#include <PubSubClient.h>

// #include <ESP32Servo.h>

// Servo myservo;

//WIFI STUFF
char ssid[] = "Plaksha-Events";
char pass[] = "Welcome@2024";

//MQTT STUFF
char *ip= "test.mosquitto.org";
int port = 1883;
char *topic = "yts2024/wise/grp12";

WiFiClient wifiClient;
PubSubClient client(wifiClient);

// #include <Servo.h>                                                                                            // could have to change as we may not use this

#define Width 128
#define Height 64
#define Reset -1
#define Address 0x3C

#define MQ135 35
#define LDR 33
#define LED 14
#define DHTPin 13
#define HallEffectPin 34
// #define ServoPin 23

#define time_for_hallEffectSensor_to_break 5

Adafruit_SSD1306 display = Adafruit_SSD1306(128, 64, &Wire,Reset); // dont write 128 and 62 else it goes to default
DHT dht = DHT(DHTPin,DHT22);

// Servo myservo;  // create servo object to control a servo                                                           //May have to change

// volatile byte revolutions;

// int pos = 0;    // variable to store the servo position

float v = 5.0;
float r2 = 10.0;
float r0 = 74.0;
float b = -2.769034857;
float a = 116.6020682;

int x = 0;
int count = 0;
unsigned long start = 0;
unsigned long timeold = 0;
int revolutions = 0;

bool check;
String HallEffectStr;
String prev_HallEffectStr;

String prev_RPM_Calculated;

// int pos = 0;

void setup() {
  Serial.begin(9600);
  pinMode(HallEffectPin, INPUT);
  // myservo.attach(ServoPin);
  dht.begin();

  SSD1306_Setup();

  pinMode(MQ135, INPUT);
  pinMode(LDR,INPUT);
  pinMode(LED,OUTPUT);
  digitalWrite(LED, LOW);
  
  WiFi.begin(ssid, pass);
  Serial.begin(9600);
  client.setServer(ip,port);
  client.connect("group12ESP32Client");

  while(WiFi.status() != WL_CONNECTED){
    Serial.println("WIFI DICONNECTED");
    display.println("Wifi DISCONNECTED");
    display.display();
  }
  display.clearDisplay();
  display.setCursor(0,0);
  display.println("Wifi CONNECTED");
  Serial.println("WIFI CONNECTED");
  
  while (!client.connected()){
    Serial.println("MQTT DISCONNECTED");
    display.println("MQTT DISCONNECTED");
    display.display();
    client.connect("group12ESP32Client");
  }
  display.clearDisplay();
  display.setCursor(0,0);
  display.println("MQTT CONNECTED");
  Serial.println("MQTT CONNECTED");
  Serial.println(WiFi.localIP());
  display.clearDisplay();
  display.setCursor(0,0);
  
  // pinMode(hall_eff, INPUT);
  // attachInterrupt(hall_eff, magnet_detect, RISING);//Initialize the intterrupt pin (Arduino digital pin 2)
  // revolutions = 0;
  // rpm = 0;
  // timeold = 0;
  // start = millis();

  // myservo.attach(9);                                                                                                   //could have to change 
}

void loop() {
  while(WiFi.status() != WL_CONNECTED){
    Serial.println("WIFI DICONNECTED");
  }
  while (!client.connected()){
    Serial.println("MQTT DISCONNECTED");
    client.connect("group12ESP32Client");
    check = false;
  }
  if(client.connected()&& check==false){
    Serial.println("Wifi n MQTT CONNECTED");
    Serial.println(WiFi.localIP());
    check = true;
  }
  printOnDisplay();

  if(analogRead(LDR)<1000){
    digitalWrite(LED, HIGH);
    for (int y=24; y<=31; y++){
      for (int x=60; x<127; x++){
        display.drawPixel(x, y, BLACK); 
      }
    }
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(60,24);
    Serial.println("LED is HIGH");
    display.println(";LED is HIGH");
    display.display();
    client.publish(topic, String("LED is HIGH").c_str());
    // for (pos = 0; pos <= 180; pos += 5) {
    //   myservo.write(pos);
    // } 
  }
  else{
    digitalWrite(LED, LOW);
    for (int y=24; y<=31; y++){
      for (int x=60; x<127; x++){
        display.drawPixel(x, y, BLACK); 
      }
    }
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(60,24);
    Serial.println("LED is LOW");
    display.println(";LED is LOW");
    display.display();
    client.publish(topic, String("LED is LOW").c_str());
    // for (pos = 1800; pos >= 0; pos -= 5) {
    //   myservo.write(pos);
    // } 
  }
  // delay(500);
  
}
long findRPM(){
  unsigned long TimeInnitially = millis()/1000;
  // int SameTimeCount = 0;
  int BeforeTime =millis();
  // int timeRepeated = (TimeInnitially + time_for_hallEffectSensor_to_break) -(BeforeTime/1000); // finaltime -secondlastfinaltime == 0
  // Serial.println(timeRightNow + "    " + millis()/1000);
  while((millis()/1000)<=(TimeInnitially + time_for_hallEffectSensor_to_break)){ // the rhs defines a set time until the function will return a -1/null
    if( ((millis()/1000) - (BeforeTime/1000)) != 0){
      String to_be_printed = ("magnet needs to be scanned before "+ String((TimeInnitially + time_for_hallEffectSensor_to_break)-(BeforeTime/1000))+" seconds");
      String to_be_printed_by_Display =("scan before "+ String((TimeInnitially + time_for_hallEffectSensor_to_break)-(BeforeTime/1000))+" seconds");
      Serial.println(to_be_printed);
      for (int y=57; y<=64; y++){
       for (int x=0; x<127; x++){
        display.drawPixel(x, y, BLACK); 
       }
      }
      display.setCursor(0,57);
      display.setTextColor(SSD1306_WHITE);
      display.println(to_be_printed_by_Display);
      display.display();
      client.publish(topic, to_be_printed.c_str());
      BeforeTime = millis();
    }
    // if(timeRepeated -((TimeInnitially + time_for_hallEffectSensor_to_break)-(BeforeTime/1000))==0){
    //   Serial.print("you have ");
    //   Serial.print((timeRTimeInnitiallyightNow + time_for_hallEffectSensor_to_break)-(BeforeTime/1000));
    //   Serial.println( " seconds left");
    //   BeforeTime = millis();
    //   timeRepeated = (TimeInnitially + time_for_hallEffectSensor_to_break)-(BeforeTime/1000);
    // }
    x = magnet_detect(HallEffectPin);
    if(x==0){
      if(revolutions == 1){
        client.publish(topic,String("waiting for magnet for the second time").c_str());
        Serial.println("waiting for magnet for the second time");
        //display.println("waiting for magnet...");
        //display.display();
        TimeInnitially = millis()/1000;
        BeforeTime = millis();
      }
      if( ((millis()/1000) - (BeforeTime/1000)) != 0 && revolutions == 1){
      String to_be_printed = ("magnet needs to be rescanned before "+ String((TimeInnitially + time_for_hallEffectSensor_to_break)-(BeforeTime/1000))+" seconds");
      Serial.println(to_be_printed);
      // display.println(to_be_printed);
      // display.display();
      client.publish(topic, to_be_printed.c_str());
      BeforeTime = millis();
      }
      if(revolutions==2){
        long RPMValue = calculateRPM();
        return RPMValue;
      }
    }
  }
  return -1;
}
long calculateRPM() {
  long rpm = (60000/(millis() - timeold));
  timeold = millis();
  revolutions = 0;
  return rpm;
}
int magnet_detect(int pin){
  int a = digitalRead(pin);
  // Serial.println("before if statement");
  if (a == 1) {
    // Serial.println("in if statement a=1 we dont want");
  }
  else {
    // Serial.println("in else statement a=0");
    unsigned long Initial_time_for_magnet_in_static = millis()/1000;
    revolutions = revolutions + 1;
    Serial.println("Magnet present");
    bool count = false;
    Serial.println("HallEffect Pin: " +digitalRead(HallEffectPin));
    while(digitalRead(HallEffectPin)==0){
      if(((millis()/1000)-Initial_time_for_magnet_in_static) > 1 && !count){
        for (int y=48; y<=55; y++){
          for (int x=0; x<127; x++){
            display.drawPixel(x, y, BLACK); 
          }
        }
        display.setCursor(0,49);
        display.setTextColor(SSD1306_WHITE);
        Serial.println("magnet is stuck");
        display.println("magnet is stuck");
        display.display();
        client.publish(topic, String("magnet is stuck").c_str());
        count = true;
      }
      Serial.println("in while loop a=0, magnet always present");
    }
    if(revolutions == 1){
      timeold = millis();
    }
    // Serial.println(millis());
  }
  return a;
}
void SSD1306_Setup(){
  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  display.begin(SSD1306_SWITCHCAPVCC, Address); // Address 0x3C for 128x32
  display.clearDisplay();
  
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);
  display.println("connected!");
  display.setCursor(0,0);
  display.display(); // actually display all of the above
  delay(1000);
  display.clearDisplay();
  display.display();
}
void printOnDisplay(){
  for (int y=0; y<=23; y++){
    for (int x=0; x<127; x++){
      display.drawPixel(x, y, BLACK); 
    }
  }
  for (int y=24; y<=31; y++){
    for (int x=0; x<60; x++){
      display.drawPixel(x, y, BLACK); 
    }
  }
  for (int y=48; y<=64; y++){
    for (int x=0; x<127; x++){
      display.drawPixel(x, y, BLACK); 
    }
  }
  display.setCursor(0,0);
  display.setTextColor(SSD1306_WHITE);
  // display.clearDisplay();
  // display.setCursor(0,0);
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  double v2 = analogRead(MQ135) * (v / 4095.0);  
  double r1 = (r2 * (v - v2)) / v2;
  double ratio = r1 / r0;
  double ppm = a*pow(ratio, b);

  String humStr = "humidity: "+ String(hum);
  display.print(humStr);
  // display.print("Humidity: ");
  // display.print(hum);
  client.publish(topic, humStr.c_str());
  Serial.println(humStr);
  // Serial.print("Humidity: ");
  // Serial.println(hum);
  display.println(" g/m^3");
  // display.display();

  display.setCursor(0,8);
  String tempStr = "Temperature: "+String(temp);
  display.print(tempStr);
  // display.print("Temperature: ");
  // display.print(temp);
  client.publish(topic, tempStr.c_str());
  Serial.println(tempStr);
  // Serial.print("Temperature: ");
  // Serial.println(temp);
  display.println(" C");
  // display.display();

  display.setCursor(0,16);
  String ppmStr = "MQ135 value: "+String(ppm);
  display.println(ppmStr);
  // display.print("MQ135 value: ");
  // display.println(ppm);
  client.publish(topic,ppmStr.c_str());
  Serial.println(ppmStr);
  // Serial.print("MQ135 value: ");
  // Serial.println(ppm);
  // display.display();
  
  display.setCursor(0,24);
  String LDRStr = "LDR: "+String(analogRead(LDR));
  Serial.println(LDRStr);
  display.println(LDRStr);
  client.publish(topic, LDRStr.c_str());
  display.display();

  for (int y=40; y<=47; y++){
    for (int x=0; x<127; x++){
      display.drawPixel(x, y, BLACK); 
    }
  }
  display.setCursor(0,40);
  display.setTextColor(SSD1306_WHITE);
  prev_HallEffectStr = ("RPM Before: " + prev_RPM_Calculated);
  display.print(prev_HallEffectStr);
  display.display();

  long RPM_Calculated = findRPM();
  String HallEffectForDisplay;
  if(RPM_Calculated == -1){
    HallEffectStr = "RPM: "+String("magnet took too long");
    HallEffectForDisplay = "RPM: "+String("magnet took time");
  }
  else{
    HallEffectStr = "RPM: "+String(RPM_Calculated);
    HallEffectForDisplay ="RPM: "+String(RPM_Calculated);
    prev_RPM_Calculated = String(RPM_Calculated);
  }
  for (int y=32; y<=39; y++){
    for (int x=0; x<127; x++){
      display.drawPixel(x, y, BLACK); 
    }
  }
  display.setCursor(0,32);
  display.setTextColor(SSD1306_WHITE);
  // display.print("RPM: ");
  display.println(HallEffectForDisplay);
  client.publish(topic, HallEffectStr.c_str());
  // Serial.print("RPM: ");
  Serial.println(HallEffectStr);
  display.display();
  
  //blank line
  client.publish(topic,String("-------------------------").c_str());
  Serial.println("-----------------");
}
