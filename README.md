# ESP8266_Network
Creating a small network to allow me to work on the microtractor project. This project is using the home router as the networking point. I first explored using an access point but have decided against it, as I feel that the home network will be more reliable in the short term.

![image](https://github.com/tomcunn/ESP8266_Network/assets/4383135/e7f3589b-3590-491d-8b6f-7ca58f2449a4)

# Protocol

LEFT_SPEED/RIGHT_SPEED: 
125 = stop
250 = Full Speed Forward
0 = Fulle Speed Reverse

Packet:
This the packet to control the speed of the vehicle and the most used packet. 
0x4D, LEFT_SPEED, RIGHT_SPEED

Packet:
When this packet is received, the ESP8266 can quit sending identification packet as the identifaction has already been logged.
0x49, 0x50, 0x4C  (IP is acknowledged)

# Links

https://stackoverflow.com/questions/39064193/esp8266-send-udp-string-to-ap
