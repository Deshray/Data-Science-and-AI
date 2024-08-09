#include <WiFi.h>
#include <PubSubClient.h>

WiFiClient wi;
PubSubClient client(wi);
String command = "";

void setup() {
  Serial.begin(115200);
  WiFi.begin("Plaksha-Events", "Welcome@2024");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.println("connected to wifi");
  client.setServer("test.mosquitto.org", 1883);
  pinMode(2, OUTPUT);

  while (!client.connected()){
    if (client.connect("LEDSUBSCRIBER")){
      Serial.println("Connected");
      client.subscribe("yts/g12/wise/led");
    }
  }
  client.setCallback(callback);
}

void callback(char* topic, byte* payload, unsigned int length) {
  delay(1000);
  Serial.println("Message received");
  for (int i = 0; i<length, i++){
    command = command + (char)payload[i];
  }
  Serial.println();
}

void loop() {
  if(!client.connected()){
    while (!client.connected()){
      if (client.connect("LEDSUBSCRIBER")){
        Serial.println("Connected");
      }
        client.subscribe("yts/g12/wise/led");
    } 
  }
  if(command=="on"){
    digitalWrite(2, HIGH);
  }
  else if (command == "off"){
    digitalWrite(2, LOW);
  }
  else{
    Serial.println("Invalid command");
  }
  client.loop()
}

