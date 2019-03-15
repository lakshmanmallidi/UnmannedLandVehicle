import time
import socket
import threading
import serial
import RPi.GPIO as GPIO
import gps
def sendfun(client):
    global flag,lat,lag,spd
    while flag:
        data = ser.readline()[:-2]
	if data.startswith("wait")!=True:
	    data=data+lat+","+lag+","+spd
            client.send(data)
    ser.close()
    client.close()
def gpsthread():
    global lat,lag,spd,flag
    while flag:
	report = gpsd.next()
	if report['class']=='TPV':
	    lat="%.6f"%report.lat
	    lag="%.6f"%report.lon
            spd="%f"%report.speed
def forward():
    GPIO.output(motor11,GPIO.HIGH)
    GPIO.output(motor12,GPIO.LOW)
    GPIO.output(motor21,GPIO.HIGH)
    GPIO.output(motor22,GPIO.LOW)
def reverse():
    GPIO.output(motor11,GPIO.LOW)
    GPIO.output(motor12,GPIO.HIGH)
    GPIO.output(motor21,GPIO.LOW)
    GPIO.output(motor22,GPIO.HIGH)
def right():
    GPIO.output(motor11,GPIO.HIGH)
    GPIO.output(motor12,GPIO.LOW)
    GPIO.output(motor21,GPIO.LOW)
    GPIO.output(motor22,GPIO.HIGH)
def left():
    GPIO.output(motor11,GPIO.LOW)
    GPIO.output(motor12,GPIO.HIGH)
    GPIO.output(motor21,GPIO.HIGH)
    GPIO.output(motor22,GPIO.LOW)
def stop():
    GPIO.output(motor11,GPIO.LOW)
    GPIO.output(motor12,GPIO.LOW)
    GPIO.output(motor21,GPIO.LOW)
    GPIO.output(motor22,GPIO.LOW)
motor11=29
motor12=31
motor21=33
motor22=35
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motor11,GPIO.OUT)
GPIO.setup(motor12,GPIO.OUT)
GPIO.setup(motor21,GPIO.OUT)
GPIO.setup(motor22,GPIO.OUT)
flag=True
lat="0"
lag="0"
spd="0"
gpsd=gps.gps(mode=gps.WATCH_ENABLE|gps.WATCH_NEWSTYLE)
ser = serial.Serial("/dev/ttyACM0")
s=socket.socket()
s.bind(("192.168.43.5",8000))
s.listen(1)
client, addr = s.accept()
threading.Thread(target=sendfun, args=(client,)).start()
threading.Thread(target=gpsthread).start()
while flag:
    cmd = client.recv(10)
    if cmd=="fw":
        forward()
    elif cmd=="rv":
        reverse()
    elif cmd=="rt":
        right()
    elif cmd=="lt":
        left()
    elif cmd=="stop":
        stop()
    elif cmd=="startd":
        ser.write("start")
    elif cmd=="stopd":
        ser.write("stop")
    elif cmd=="exit!!":
        stop()
	ser.write("stop")
        flag=False
GPIO.cleanup()
s.close()
        
