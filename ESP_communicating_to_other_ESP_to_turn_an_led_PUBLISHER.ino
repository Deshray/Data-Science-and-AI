#include <WiFi.h>
#include <PubSubClient.h>

const char* wifiname = "Plaksha-Events";
const char* wifipass ="Welcome@2024";

const char* server = "test.mosquitto.org";

WiFiClient espClient;
PubSubClient client = PubSubClient(espClient);

bool check;

void setup() {
  Serial.begin(9600);
  WiFi.begin(wifiname,wifipass);

  while(WiFi.status() != WL_CONNECTED){
    Serial.println("WIFI DICONNECTED");
    delay(500);
  }
  Serial.println("WIFI CONNECTED");
  client.setServer(server,1883);

  while(!client.connected()){
    Serial.println("MQTT DISCONNECTED");
    client.connect("grp12LEDPublisher");
    delay(500);
  }
  Serial.println("MQTT CONNECTED");
}

void loop() {
  while(WiFi.status() != WL_CONNECTED){
    Serial.println("WIFI DICONNECTED");
  }
  while (!client.connected()){
      Serial.println("MQTT DISCONNECTED");
      client.connect("grp12LEDPublisher");
      check = false;
  }
  if(client.connected()&& check==false){
    Serial.println("MQTT CONNECTED");
    Serial.println(WiFi.localIP());
    check = true;
  }
  if(!client.connected()){
    while(!client.connected()){
      client.connect("grp12LEDPublisher");
      delay(500);
    }
  }
  
  // client.loop();//u dont have to continuously repeat the wifi connection and mqtt connection like in prototype 1
  if(Serial.available()>0){
    String msg = Serial.readString();
    msg.trim();
    Serial.println("before : " + msg );
    if(msg.equalsIgnoreCase("on") || msg.equalsIgnoreCase("off")){
      client.publish("yts2024/wise/grp12",msg.c_str());
      Serial.println(msg);
    }
    delay(1000);
  }  
}
