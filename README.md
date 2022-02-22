# GPS-Receiver-SDR-on-GNURadio
A real-time GPS Software defined receiver based on gnuradio

Only acqusition part is completed. 

# Introduction
This is a project trying to use gnuradio to create a realtime gps software defined receiver. This project will be simple to use if a gnuradio is firstly installed. With the multiple source supported by gnuradio, you can easily employ kinds of hardwares like hackrf, usrp, bladeRf, etc.
Procedures are separated into acqutsition, tracking, navigation solution part to satisfy the needs of experiment on a certain block.

# How to use
Simply download the .grc files and open it with gnunradio. The code of embeded python block is also provided. In case of unsuccessful opening, you can create your own flow graph same as the .grc file and copy and paste the python code to embeded python block.

# acqusition block
![image]https://github.com/Mortarboard-H/GPS-Receiver-SDR-on-GNURadio/blob/main/acqusition/acqusiton%20graph.png
