#include "Arduino.h"
#include "Wire.h"
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "DFRobotIRPosition.h"


const char *ssid = "****";
const char *password = "****";

WiFiUDP Udp;
WiFiClient client;
unsigned int localUdpPort = 5000; // local port to listen on

IPAddress SendIP(192,168,0,173);


char incomingPacket[255]; // buffer for incoming packets
char replyPacket[] = "I am the camera"; // a reply string to send back

void connectToWiFi() 
{
   //Connect to WiFi Network
   Serial.print("Connecting to WiFi");
   Serial.println("...");
   WiFi.begin(ssid, password);
   int retries = 0;
   while ((WiFi.status() != WL_CONNECTED) && (retries < 15)) 
   {
      retries++;
      digitalWrite(BUILTIN_LED, HIGH);
      delay(500);
      digitalWrite(BUILTIN_LED, LOW);
      delay(500);
      Serial.print(".");
   }
   if (retries > 14) 
   {
      Serial.println(F("WiFi connection FAILED"));
   }
   if (WiFi.status() == WL_CONNECTED) 
   {
      Serial.println(F("WiFi connected!"));
      Serial.println("IP address: ");
      Serial.println(WiFi.localIP());
      digitalWrite(BUILTIN_LED, HIGH);
   }
   Serial.println("Setup ready");
}
   

void setup()
{ 
  Serial.begin(115200);
  
  delay(3000);
  
  pinMode(BUILTIN_LED,OUTPUT);
  connectToWiFi();
}

void loop()
{
  //static int packetRecieved = false;
  //char buf[3];
  //static int counter = 48;
  
  //Sending a packet
  Serial.println("Sending response packet");
  Udp.beginPacket(SendIP,localUdpPort);
  Udp.write(replyPacket);
  Udp.endPacket();
  

  ////Check to see if a packet has come in the door
  //int packetSize = Udp.parsePacket();
  //
  ////If the packet is present
  //if (packetSize)
  //{
  //  Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
  //  int len = Udp.read(incomingPacket, 255);
  //  if (len > 0)
  //  {
  //   incomingPacket[len] = '\0';
  //  }
  //  Serial.printf("UDP packet contents: %s\n", incomingPacket);
  //
  //
  //
  //  packetRecieved = true;
  //}
  delay(100);
}
