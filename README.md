# GPS-Receiver-SDR-on-GNURadio
A real-time GPS Software defined receiver based on gnuradio

Only acqusition part is completed. 

# Introduction
This is a project trying to use gnuradio to create a realtime gps software defined receiver. This project will be simple to use if a gnuradio is firstly installed. With the multiple source supported by gnuradio, you can easily employ kinds of hardwares like hackrf, usrp, bladeRf, etc.
Procedures are separated into acqutsition, tracking, navigation solution part to satisfy the needs of experiment on a certain block.

# How to use
Simply download the .grc files and open it with gnunradio. The code of embeded python block is also provided. In case of unsuccessful opening, you can create your own flow graph same as the .grc file and copy and paste the python code to embeded python block.

# acqusition block
![image](https://github.com/Mortarboard-H/GPS-Receiver-SDR-on-GNURadio/blob/main/acqusition/acqusiton%20graph.png)
Two parametes are defined for the application 'samp_rate' and 'vectorLen'. 'samp_rate' defines the sample rate of the source. vectorLen is samp_rate/1e3, referring to the number of samples per code.<br>
Six blocks are used.<br>
Source: this grc uses file source, which refers to a gps signal file. It can be replaced by kinds of hardware sources as you like<br>
Throttle: essential if a file source is used. As explained by official tutorials, this block limits the excuting speed of the whole flow.<br>
Stream to Vector: convert stream of data to vectors of data.<br>
GPS Acqusition: this is a 'Embeded Python Block'. Code of this block is provided in epy_block_0.py. refering [embeded python block tutorial](https://wiki.gnuradio.org/index.php?title=Creating_Your_First_Block) for further imformation of this block.<br>
Vector to stream: convert vectors of data back to stream<br>
Time Sink: to visialize the data stream<br>
