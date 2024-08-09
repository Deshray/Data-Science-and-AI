#include <WiFi.h>
#include <PubSubClient.h>

//WIFI STUFF
char ssid[] = "Plaksha-Events";
char pass[] = "Welcome@2024";

//MQTT STUFF
char *ip= "test.mosquitto.org";
int port = 1883;
char *topic = "yts2024/wise/grp12";

#define LEDPin 2

WiFiClient wifiClient;
PubSubClient client(wifiClient);

String command = "";

void setup()
{
 WiFi.begin(ssid, pass);
 Serial.begin(9600);
 client.setServer(ip,port);
 client.setCallback(callback);
 client.connect("group12ESP32Client");
 client.subscribe(topic);
 pinMode(LEDPin, OUTPUT);
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
    client.connect("group3ESP32Client");
    client.subscribe(topic);
  }

  client.loop();

  if(command == "on"){
    digitalWrite(LEDPin, HIGH);
  }
  else if(command == "off"){
    digitalWrite(LEDPin, LOW);
  }

  //Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  command = "";
  Serial.println("Message arrived");
  for (int i=0;i<length;i++) {
    command = command + ((char)payload[i]);
  }
  Serial.println(command);
}