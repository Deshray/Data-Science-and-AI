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
client.setCallback(callback);
client.connect("group12ESP32Client");
client.subscribe(topic);
}

void loop () {
  if(WiFi.isConnected()){
    //Serial.println("WIFI CONNECTED");
  }
  else{
    Serial.println("WIFI DISCONNECTED");
    WiFi.begin(ssid, pass);
  }

  if(client.connected()){
    //Serial.println("MQTT CONNECTED");
  }
  else{
    Serial.println("MQTT DISCONNECTED");
    client.connect("group12ESP32Client");
    client.subscribe(topic);
  }

  //Serial.println(WiFi.localIP());

  client.loop();
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i=0;i<length;i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}