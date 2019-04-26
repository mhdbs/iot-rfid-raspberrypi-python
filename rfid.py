import RPi.GPIO as GPIO
import serial
import time
import datetime
import requests
import spidev
import os
import urllib2

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0,0)

def getReading(channel):
    rawData = spi.xfer([1, (8 + channel) << 4, 0])
    processedData = ((rawData[1]&3) << 8) + rawData[2]
    return processedData

url='{YOUR_URL}'

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

while True:
    string = ser.read(12)
    
    if len(string) == 0:
        print "Please insert a tag"
        continue
    else:
        data = string[1:11] #exclude start x0A and stop x0D bytes
        res=requests.post(url + "&s0=%s"% (string))
        if string == '4A007BF4E025': 
            print "student 1"
            print(string)
            print("Last valid input: " + str(datetime.datetime.now()))
            time.sleep(1)
            GPIO.output(11,True)
            time.sleep(3)
            GPIO.output(11,False) 
            time.sleep(1)
        elif string == '0000A6C13255':
            print "student 2"
            print(string)
            print("Last valid input: " + str(datetime.datetime.now()))
            time.sleep(1)
            GPIO.output(11,True)
            time.sleep(3)
            GPIO.output(11,False) 
            time.sleep(1)
        else:
            print "You do not have a valid tag"
            print("Last valid input: " + str(datetime.datetime.now()))
            GPIO.output(13,True)
            time.sleep(3)
            GPIO.output(13,False) 
            time.sleep(1)
            

