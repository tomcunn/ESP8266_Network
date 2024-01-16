//********************************************
//
//   Writing the Tractor ID to EEROM
//
//
//*********************************************
#include "EEPROM.h"

#define SIZE 64

char TRACTOR_ID = 0x31;  //ASCII "1"
char myData[3];


void setup() 
{
    Serial.begin(115200);
    Serial.println("Starting Program");
    EEPROM.begin(SIZE);
    delay(100);
    
    myData[0] = EEPROM.read(0);
    myData[1] = EEPROM.read(1);
    myData[2] = EEPROM.read(2);

    Serial.println("Data from EEROM");
    Serial.println(myData);
}

void loop() 
{
    Serial.println(myData);
    delay(1000);
}
