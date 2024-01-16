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
    //Address 2 holds the value of the tractor ID
    EEPROM.write(0,0x49);       // "I"
    EEPROM.write(1,0x44);       // "D"
    EEPROM.write(2,TRACTOR_ID); // "ID of TRACTOR"
    delay(100);
    EEPROM.commit(); 
    
    Serial.println("Data has been written");
    delay(1000);
    
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
