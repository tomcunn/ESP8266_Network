#include "Arduino.h"
#include "Wire.h"
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "DFRobotIRPosition.h"

IPAddress local_IP(192,168,4,1);
IPAddress gateway(192,168,4,9);
IPAddress subnet(255,255,255,0);

WiFiUDP Udp;
unsigned int localUdpPort = 5000; // local port to listen on

char incomingPacket[255]; // buffer for incoming packets
char replyPacket[] = "I am the server"; // a reply string to send back


void setup()
{ 
  Serial.begin(115200);
  
  delay(3000);
  
  pinMode(BUILTIN_LED,OUTPUT);

  Serial.print("Setting soft-AP configuration ... ");
  Serial.println(WiFi.softAPConfig(local_IP, gateway, subnet) ? "Ready" : "Failed!");

  Serial.print("Setting soft-AP ... ");
  Serial.println(WiFi.softAP("IR_Camera") ? "Ready" : "Failed!");

  Serial.print("Soft-AP IP address = ");
  Serial.println(WiFi.softAPIP());

  while (WiFi.softAPgetStationNum()== 0)
  {
    delay(3000);
    Serial.println("Wait for client");
  }

  Serial.printf("Stations connected to soft-AP = %d\n", WiFi.softAPgetStationNum());
  Serial.print("Soft-AP IP address = ");
  Serial.println(WiFi.softAPIP());
  Serial.printf("MAC address = %s\n", WiFi.softAPmacAddress().c_str());

  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.softAPIP().toString().c_str(), localUdpPort);

  delay(1000);
}

void loop()
{
  static int packetRecieved = false;
  char buf[3];
  static int counter = 48;
  
  //Check to see if a packet has come in the door
  int packetSize = Udp.parsePacket();
  
  //If the packet is present
  if (packetSize)
  {
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(incomingPacket, 255);
    if (len > 0)
    {
     incomingPacket[len] = '\0';
    }
    Serial.printf("UDP packet contents: %s\n", incomingPacket);


    //Send a response packet
    Serial.println("Sending response packet");
    Udp.beginPacket(Udp.remoteIP(),Udp.remotePort());
    Udp.write(replyPacket);
    Udp.endPacket();
    packetRecieved = true;
  }
}
