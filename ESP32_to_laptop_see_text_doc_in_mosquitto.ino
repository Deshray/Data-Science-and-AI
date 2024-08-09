#include <WiFi.h>
#include <PubSubClient.h>

//WIFI STUFF
char ssid[] = "Plaksha-Events";
char pass[] = "Welcome@2024";

//MQTT STUFF
char *ip= "test.mosquitto.org";
int port = 1883;
char *topic = "yts2024/wise/grp12";

WiFiClient wifiClient;
PubSubClient client(wifiClient);

bool check;

void setup()
{
 WiFi.begin(ssid, pass);
 Serial.begin(9600);
 client.setServer(ip,port);
 client.connect("group12ESP32Client");
 while(WiFi.status() != WL_CONNECTED){
  Serial.println("WIFI DICONNECTED");
 }
 Serial.println("WIFI CONNECTED");
 while (!client.connected()){
    Serial.println("MQTT DISCONNECTED");
    client.connect("group12ESP32Client");
    check=false;
 }
 check=true;
 Serial.println("MQTT CONNECTED");
 Serial.println(WiFi.localIP());
}

void loop () {
  while(WiFi.status() != WL_CONNECTED){
    Serial.println("WIFI DICONNECTED");
  }
  while (!client.connected()){
      Serial.println("MQTT DISCONNECTED");
      client.connect("group12ESP32Client");
      check = false;
  }
  if(client.connected()&& check==false){
    Serial.println("MQTT CONNECTED");
    Serial.println(WiFi.localIP());
    check = true;
  }
  if(Serial.available()>0){
    String userInput = Serial.readString();
    client.publish(topic,userInput.c_str());
    Serial.println(userInput.c_str());
    Serial.println("Enter the string: ");
    delay(1000);
  }
  
}

// char* ConvertStringToCharArray(String S)
// {
//   int   ArrayLength  =S.length()+1;    //The +1 is for the 0x00h Terminator
//   char  CharArray[ArrayLength];
//   S.toCharArray(CharArray,ArrayLength);

//   return(CharArray);
// }