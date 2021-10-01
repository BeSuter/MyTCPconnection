Toy project testing a TCP connection between my MacBook and my Raspberry Pi.
Everytime my MacBook "Pings" the Raspberry Pi, the Raspberry Pi will send one frame from the Lepton3.5 thermal camera
back to the MacBook. Each pixel contains the corresponding temperature value in C (still has to be calibrated).

ToDo:
Add a timestamp to each frame, so we can calibrate the livestream...
--> Look up how queue.Queue works (BUF_SIZE...)
--> Look up if we can easily add timestamps to libuvc stream.