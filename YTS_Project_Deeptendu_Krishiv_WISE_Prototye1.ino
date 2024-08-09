#include <DHT.h>
#include <DHT_U.h>
#include <Wire.h>

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define Width 128
#define Height 64
#define Reset -1
#define Address 0x3C

Adafruit_SSD1306 display = Adafruit_SSD1306(Width,Height, &Wire,Reset);
DHT dht = DHT(5,DHT22);
float v = 5.0;
float r2 = 10.0;
float r0 = 74.0;
float b = -2.769034857;
float a = 116.6020682;

#define MQ135 34
#define LDR 35
#define LED 33

void setup() {
  Serial.begin(9600);
  dht.begin();

  pinMode(MQ135, INPUT);
  pinMode(LDR,INPUT);
  pinMode(LED,OUTPUT);
  digitalWrite(LED, LOW);

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
void loop() {
  display.clearDisplay();
  display.setCursor(0,0);
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  double v2 = analogRead(MQ135) * (v / 4095.0);  
  double r1 = (r2 * (v - v2)) / v2;
  double ratio = r1 / r0;
  double ppm = a*pow(ratio, b);
  display.print("Humidity: ");
  display.print(hum);
  Serial.print("Humidity: ");
  Serial.println(hum);
  display.println(" g/m^3");
  display.print("Temperature: ");
  display.print(temp);
  Serial.print("Temperature: ");
  Serial.println(temp);
  display.println(" C");
  display.print("MQ135 value: ");
  display.println(ppm);
  Serial.print("MQ135 value: ");
  Serial.println(ppm);
  display.print("LDR: ");
  display.println(analogRead(LDR));
  Serial.print("LDR: ");
  Serial.println(analogRead(LDR));

  display.display();
  if(analogRead(LDR)<1000){
    digitalWrite(LED, HIGH);
  }
  else{
    digitalWrite(LED, LOW);
  }
  delay(500);
}

