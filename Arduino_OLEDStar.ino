#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  display.clearDisplay();
  display.drawLine(64, 10, 70, 30, SSD1306_WHITE);
  display.drawLine(70, 30, 90, 30, SSD1306_WHITE);
  display.drawLine(90, 30, 74, 45, SSD1306_WHITE);
  display.drawLine(74, 45, 80, 60, SSD1306_WHITE);
  display.drawLine(80, 60, 64, 50, SSD1306_WHITE);
  display.drawLine(64, 50, 48, 60, SSD1306_WHITE);
  display.drawLine(48, 60, 54, 45, SSD1306_WHITE);
  display.drawLine(54, 45, 38, 30, SSD1306_WHITE);
  display.drawLine(38, 30, 58, 30, SSD1306_WHITE);
  display.drawLine(58, 30, 64, 10, SSD1306_WHITE);

  display.display();
}

void loop() {
  // put your main code here, to run repeatedly:
}
