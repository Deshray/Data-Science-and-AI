#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

DHT dht(5, DHT22);
float v = 5.0;
float r2 = 10.0;
float r0 = 74.0;
float b = -2.765034857;
float a = 116.6020682;

void setup() {
  Serial.begin(115200);
  dht.begin();
  display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS);
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  pinMode(34, INPUT);
  pinMode(35, INPUT);
  pinMode(13, OUTPUT);
}

void loop() {
  display.clearDisplay();
  display.setCursor(0, 10);
  float hum = dht.readHumidity();
  float temp = dht.readTemperature();
  float val = analogRead(34);  
  float v2 = map(val, 0, 4095, 0, 100);
  float r1 = (r2 * (v - v2)) / v2;
  float ratio = r1 / r0;
  float ppm = a * pow(ratio, b);
  int a = analogRead(34);
  if (a<150){
  digitalWrite(13,HIGH);
  display.println("It's dark")
}
  else{
  digitalWrite(13, LOW);
  display.println("It's bright")
}
  display.print("Humidity: ");
  display.print(hum);
  display.println(" %");
  display.print("Temperature: ");
  display.print(temp);
  display.println(" C");
  display.print("MQ135 value: ");
  display.println(ppm);
  display.display();
  delay(500);
}
