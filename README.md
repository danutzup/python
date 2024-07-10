# python
Some python code I am using and writting.
So searching I have found in internet following python code and pages related to raspberry pi and ST7920 lcd conected using spi :
http://www.astromik.org/raspi/42.htm
https://github.com/SrBrahma/RPi-12864-LCD-ST7920-lib/tree/master
And I did with the help of ChatGPT transform that python code in a library that can be used in any python code to display on this lcd text data. 
For connection schematic see glcd12864-sch.gif

In my enviroment I have multiple esp8266 running tasmota firmware that are pushing to a mosquito server 
with nodejs running. 
The program  mqtt_rasp_lcd.py  in this repository is running on a raspberry pi zero w with  ST7920 lcd connected
and I am displaying temperature and humidity that are in the main mosquito server pushed by nultiple esp8266 wiyh DHT and SHT sensors.
