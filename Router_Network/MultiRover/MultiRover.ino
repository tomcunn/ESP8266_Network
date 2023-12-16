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

//******************************************************************
//Set the name of the tractor here, could use EEROM!!

char replyPacket[] = "Rover_Grey"; // a reply string to send back
const char *ssid = "***********";
const char *password = "**********";

//********************************************************************

//Configure the PWM chip for the tractor
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x52);

//IP address of the computer you are connecting to
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

int DeterminePercent(int percent)
{
  int value;

  value = (int16_t)(((int32_t)percent * 4095) / 125);
  return value;
}

void setup_motors()
{
  //Set Frequency for PCA chip
  Wire.begin(pwmSDA, pwmSCL);
  pwm.begin();
  pwm.setPWMFreq(200);
  
  //Drive Motor Right
  pinMode(D6, OUTPUT);
  pinMode(D5, OUTPUT);
  digitalWrite(D6, LOW);
  digitalWrite(D5, LOW);
  pwm.setPWM(8, 4096, 0);

  //Drive Motor Left
  pinMode(D7, OUTPUT);
  pinMode(D8, OUTPUT);
  digitalWrite(D7, LOW);
  digitalWrite(D8, LOW);
  pwm.setPWM(9, 4096, 0);
}

void ProcessMotionControl(byte LeftCommand, byte RightCommand)
{
  //Take off the offset, the value should be between -100 and 100
  int LeftPercent = LeftCommand - 125;
  int RightPercent = RightCommand -125;
  int value = 0;
  
  //****************LEFT SIDE***************
  
  value = DeterminePercent(abs(LeftPercent));
  
 /* Serial.print(LeftPercent);
  Serial.print(",");
  Serial.print(LeftCommand);
  Serial.print(",");
  Serial.println(value);
  */
  if(LeftPercent < 0)
  {
    digitalWrite(D6, LOW);
    digitalWrite(D5, HIGH);
    pwm.setPWM(8, 0, value);

  }
  else if(LeftPercent > 0)
  {
    digitalWrite(D5, LOW);
    digitalWrite(D6, HIGH);
    
    pwm.setPWM(8,  0, value);
  }
  else
  {
    digitalWrite(D6, LOW);
    digitalWrite(D5, LOW);
    pwm.setPWM(8, 4096, 0);
  }

  //****************RIGHT SIDE**************
  value = DeterminePercent(abs(RightPercent));
  
  //Reverse
  if(RightPercent < 0)
  {
    digitalWrite(D7, LOW);
    digitalWrite(D8, HIGH);
    pwm.setPWM(9, 0, value);
  }
  //Forward
  else if(RightPercent > 0)
  {
    digitalWrite(D8, LOW);
    digitalWrite(D7, HIGH);
    pwm.setPWM(9,  0, value);
  }
  //Stop
  else
  {
    digitalWrite(D7, LOW);
    digitalWrite(D8, LOW);
    pwm.setPWM(9, 4096, 0);
  }
}
   

void setup()
{ 
  Serial.begin(115200);
 
  delay(3000);

  setup_motors();
  
  pinMode(BUILTIN_LED,OUTPUT);
  connectToWiFi();

  delay(1000);

  Udp.begin(5000);

  delay(1000);
}

void loop()
{
  static bool IP_registered = false;
  
  //Send the Identification packet
  if(!IP_registered)
  {
    Udp.beginPacket(SendIP,localUdpPort);
    Udp.write(replyPacket);
    Udp.endPacket();
  }
  
  //Check to see if a packet has come in the door
  int packetSize = Udp.parsePacket();
 
  //If the packet is present
  if (packetSize)
  { 
    //Create an array to hold the data
    byte incoming_data[packetSize];
    int len = Udp.read(incomingPacket, Udp.remotePort());

    if(incomingPacket == "IP_OK")
    {
      IP_registered = 1;
    }
    else if(incomingPacket[0] = 0x10)
    {
      //Process travel direction
      ProcessMotionControl(incomingPacket[1],incomingPacket[2]);
    }
  }
  delay(100);
}
