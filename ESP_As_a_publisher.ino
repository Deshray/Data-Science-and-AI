#include <WiFi.h>
#include <PubSubClient.h>

//WIFI STUFF
char ssid[] = "Plaksha-Events";
char pass[] = "Welcome@2024";

//MQTT STUFF
char *ip= "test.mosquitto.org";
int port = 1883;
char *topic = "yts2024/wise/grp3";

WiFiClient wifiClient;
PubSubClient client(wifiClient);

void setup()
{
 WiFi.begin(ssid, pass);
 Serial.begin(9600);
 client.setServer(ip,port);
 client.connect("group3ESP32Client");
}

void loop () {
  if(WiFi.isConnected()){
    Serial.println("WIFI CONNECTED");
  }
  else{
    Serial.println("WIFI DISCONNECTED");
    WiFi.begin(ssid, pass);
  }

  if(client.connected()){
    Serial.println("MQTT CONNECTED");
  }
  else{
    Serial.println("MQTT DISCONNECTED");
    client.connect("group3ESP32Client");
  }
  Serial.println(WiFi.localIP());

  client.publish(topic, "IT FUCKING WORKS");

  delay(1000);
}