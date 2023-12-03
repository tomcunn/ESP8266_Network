
#include "Arduino.h"
#include "Wire.h"
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "DFRobotIRPosition.h"

//IPAddress local_IP(192,168,4,1);
//IPAddress gateway(192,168,4,9);
//IPAddress subnet(255,255,255,0);

WiFiUDP Udp;
unsigned int localUdpPort = 5000; // local port to listen on
char incomingPacket[255]; // buffer for incoming packets
char replyPacket[] = "I am the rover"; // a reply string to send back


void setup()
{ 
  Serial.begin(115200);
  
  delay(3000);
  
  pinMode(BUILTIN_LED,OUTPUT);
  
  WiFi.begin("IR_Camera");
  Serial.println();
  Serial.print("Wait for WiFi");

  //Connect to the AccessPoint
  while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: " + WiFi.localIP().toString());

  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.softAPIP().toString().c_str(), localUdpPort);

  delay(1000);
}

void loop()
{
  Udp.beginPacket("192.168.4.1", UDPPort);//send ip to server
  Udp.write(replyPacket);
  Udp.endPacket();

  delay(1000);

}