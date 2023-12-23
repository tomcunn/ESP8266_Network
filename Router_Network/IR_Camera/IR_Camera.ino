#include "Arduino.h"
#include "Wire.h"
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "DFRobotIRPosition.h"

//*******************************************************************
char replyPacket[] = "IR_Camera"; // a reply string to send back
const char *ssid = "***";
const char *password = "***";
//******************************************************************

WiFiUDP Udp;
WiFiClient client;
unsigned int localUdpPort = 5000; // local port to listen on

DFRobotIRPosition myDFRobotIRPosition;

int positionX[4];     ///< Store the X position
int positionY[4];     ///< Store the Y position


//IP Address of the computer
IPAddress SendIP(192,168,0,173);


char incomingPacket[255]; // buffer for incoming packets


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

  // Begin listening to UDP port
  Udp.begin(localUdpPort);
  Serial.print("Listening on UDP port ");
  Serial.println(localUdpPort);


  //Start the camera
  myDFRobotIRPosition.begin();

  delay(1000);
}

void loop()
{
  static bool IP_registered = false;
  
  //Send the Identification packet
  if(!IP_registered)
  {
    delay(1000);
    Udp.beginPacket(SendIP,localUdpPort);
    Udp.write(replyPacket);
    Udp.endPacket();
  }
  
  ////Check to see if a packet has come in the door
  int packetSize = Udp.parsePacket();
  //
  ////If the packet is present
  if (packetSize)
  {
    //Create an array to hold the data
    char incoming_data[packetSize];
    int len = Udp.read(incomingPacket, 255);
    if((incoming_data[0] == 0x49) && (incoming_data[1] == 0x50) && (incoming_data[2] == 0x4C))
    {
      IP_registered = 1;
      Serial.println("IP_OK");
    }
  }
  
  GetPosition();
  
}

void GetPosition()
{
  char buf[8];
  static int counter = 48;
  
  //Start the IR sensor
  myDFRobotIRPosition.requestPosition();
  if (myDFRobotIRPosition.available()) 
  {
    for (int i=0; i<4; i++) 
    {
      positionX[i]=myDFRobotIRPosition.readX(i);
      positionY[i]=myDFRobotIRPosition.readY(i);
    }
  }
  counter ++;
  if(counter > 57)
  {
    counter = 48;
  }

  Serial.print(positionX[0]);
  Serial.print(",");
  Serial.println(positionY[0]);

  //Convert the int to a byte array to be sent over UDP
  buf[0] = 0x80;
  buf[1] = (char)(positionX[0] & 0xFF);
  buf[2] = (char)((positionX[0] & 0xFF00) >> 8);
  buf[3] = (char)58;
  buf[4] = (char)(positionY[0] & 0xFF);
  buf[5] = (char)((positionY[0] & 0xFF00) >> 8);
  buf[6] = (char)58;
  buf[7] = (char)counter;

  Udp.beginPacket(SendIP,localUdpPort);
  Udp.write(buf);
  Udp.endPacket();
}
