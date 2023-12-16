#include "Arduino.h"
#include "Wire.h"
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "DFRobotIRPosition.h"
#include <Servo.h>
#include <Adafruit_PWMServoDriver.h>

#define PIN D3
#define pwmSDA D2
#define pwmSCL D1

#define MIN_PULSE_WIDTH       450
#define MAX_PULSE_WIDTH       2450
#define DEFAULT_PULSE_WIDTH   1500
#define FREQUENCY             200

######################## FILL THIS OUT ##############################
const char *ssid = "*********";
const char *password = "**********";
//Set the name of the tractor here, could use EEROM!!
char replyPacket[] = "Rover_Grey"; // a reply string to send back
#####################################################################
//Configure the PWM chip for the tractor
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x52);


IPAddress SendIP(192,168,0,173);



WiFiUDP Udp;
WiFiClient client;
unsigned int localUdpPort = 5000; // local port to listen on

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
   Serial.println(F("Setup ready"));
}
   

void setup()
{ 
  Serial.begin(115200);
  
  delay(3000);
  
  //Set Frequency for PCA chip
  Wire.begin(pwmSDA, pwmSCL);
  pwm.begin();
  pwm.setPWMFreq(200);
  
  //Drive motor
  pinMode(D6, OUTPUT);
  pinMode(D5, OUTPUT);
  digitalWrite(D6, LOW);
  digitalWrite(D5, LOW);
  
  pinMode(BUILTIN_LED,OUTPUT);
  connectToWiFi();

  delay(1000);

  Udp.begin(5000);

  delay(1000);
}

void loop()
{
  static int packetRecieved = false;
  char buf[3];
  static int counter = 48;
  
  Udp.beginPacket(SendIP,localUdpPort);
  Udp.write(replyPacket);
  Udp.endPacket();
  
  //Check to see if a packet has come in the door
  int packetSize = Udp.parsePacket();
  Serial.println(packetSize);
  
  //If the packet is present
  if (packetSize)
  {
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(incomingPacket, Udp.remotePort());
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
  delay(100);
}
