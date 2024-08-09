#include <WiFi.h>

char ssid[] = "Lol"; 
char pass[] = "12345678";

WiFiClient espClient;
PubSubClient client = PubSubClient(espClient);

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, pass);
  Serial.println("\nConnecting");

  while(WiFi.status() != WL_CONNECTED){
      Serial.print(".");
      delay(100);
  }

  Serial.println("\nConnected to the WiFi network");
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  Serial.println("\nConnected to the WiFi network");
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());
  delay(1000);
}
