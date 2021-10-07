Toy project testing a TCP connection between my MacBook and my Raspberry Pi.
Everytime my MacBook pings the Raspberry Pi with a temperature value, the Raspberry Pi will send one frame from the 
Lepton3.5 thermal camera containing (xPosition, yPosition, temperature) information of every pixel with temperature 
above or equal to the pinged version back to the MacBook... Each pixel contains the corresponding temperature value 
in C (still has to be calibrated).

ToDo:
Make everything more robust...