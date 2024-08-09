#include <WiFi.h>
#include <PubSubClient.h>

char ssid[] = "Lol"; 
char pass[] = "12345678";

const char *mqtt_broker = "test.mosquitto.org";                                                                         //
const char *topic = "yts2024/wise/grp3";                                                                         //                                                                       //
const int mqtt_port = 1883;                                                                         //

WiFiClient espClient;
PubSubClient client = PubSubClient(espClient);

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid,pass);
  client.setServer(mqtt_broker,1883);
  client.setCallback(callback);
  client.connect("group12Client");
  client.subscribe(topic); 

  while (WiFi.status() != WL_CONNECTED) {
    //delay(500);
    //Serial.println("Connecting to WiFi..");
  }
  Serial.println("Wifi connected");
  while(!client.connected()){
    client.setServer(mqtt_broker,1883);
    client.setCallback(callback);
    client.connect("group12Client");
    Serial.println("Client not connected");
    delay(500);
  }
  //Serial.println("client connected");
}
void callback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message arrived in topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    for (int i = 0; i < length; i++) {
        Serial.print((char) payload[i]);
    }
    Serial.println();
    Serial.println("-----------------------");
}

void loop() {
  client.loop();

}
