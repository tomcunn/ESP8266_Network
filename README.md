# ESP8266_Network
Creating a small network to allow me to work on the microtractor project. This project is using the home router as the networking point. I first explored using an access point but have decided against it, as I feel that the home network will be more reliable in the short term.

![image](https://github.com/tomcunn/ESP8266_Network/assets/4383135/e7f3589b-3590-491d-8b6f-7ca58f2449a4)

# Protocol

LEFT_SPEED/RIGHT_SPEED: 

| Description  | Value    | 
|--------------|----------|
| Stop         | 125      |
| Full Foward  | 250      |
| Full Reverse |   0      |

Motion Packet:
This the packet to control the speed of the vehicle and the most used packet. 

| Description  | Byte Position    | 
|--------------|------------------|
| 0x4D (M)     | 1      |
| LEFT_SPEED   | 2      |
| RIGHT_SPEED  | 3      |



Packet:
When this packet is received, the ESP8266 can quit sending identification packet as the identifaction has already been logged.
0x49, 0x50, 0x4C  (IP is acknowledged)

# Links

https://stackoverflow.com/questions/39064193/esp8266-send-udp-string-to-ap
