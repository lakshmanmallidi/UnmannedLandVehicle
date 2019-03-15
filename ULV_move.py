import socket
from pynput.keyboard import Key,Listener
import threading
import pickle
import time
import matplotlib.pyplot as plt
import math
def on_press(key):
    global flag,s,b
    cmd=str(key)
    if(cmd=="u'g'"):
        b=[]
        tm=time.time()
        s.send("startd")
    elif(cmd=="u'h'"):
        s.send("stopd")
    elif(key == Key.esc):
        s.send("exit!!")
        flag=False
        return False
def listenkb():
    with Listener(on_press=on_press) as listener:
        listener.join()
def draw():
    global b
    angles=[0,30,60,90,120,150,180,180,150,120,90,60,30,0]
    dist=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    while flag:
        timearr=[]
        temp=[]
        moisture=[]
        humidity=[]
        smoke=[]
        rain=[]
        lat=[]
        lag=[]
        speed=[]
        x=[]
        y=[]
        for e in b:
            moisture.append(e[14])
            rain.append(e[15])
            smoke.append(e[16])
            humidity.append(e[17])
            temp.append(e[18])
            lat.append(e[19])
            lag.append(e[20])
            speed.append(e[21])
            timearr.append(e[22])
        if len(b)>1:
            dist=b[-1][:14]
            for i in range(14):
                x.append(dist[i]*math.cos(angles[i]))
                y.append(dist[i]*math.sin(angles[i]))
        plt.figure(1)
        plt.cla()
        plt.scatter(0,0,c="b",s=75,marker="^",label="Rover")
        plt.scatter(x,y,c='r',label="distance vectors")
        plt.legend(loc="upper left")
        plt.figure(2)
        plt.cla()
        plt.scatter(lat,lag,c='r')
        plt.xlabel('latitude----->')
        plt.ylabel('longitude----->')
        plt.figure(3)
        plt.cla()
        plt.plot(timearr,temp,c='b',label="temperature(c)")
        plt.plot(timearr,moisture,c='g',label="moisture(%)")
        plt.plot(timearr,humidity,c='r',label="humidity(%)")
        plt.plot(timearr,smoke,c='c',label="air_quality(%)")
        plt.plot(timearr,rain,c='m',label="rain(%)")
        plt.plot(timearr,speed,c='y',label="speed(km/h)")
        plt.legend(loc='upper left')
        plt.xlabel('time---->(seconds)')
        plt.ylabel('magnitudes------->')
        plt.pause(0.01)
    plt.close("all")
f=open("trainedclf.pkl","rb")
clf=pickle.load(f)
f.close()
s=socket.socket()
s.connect(("192.168.43.5",8000))
flag=True
oldstate=""
b=[]
tm=0
threading.Thread(target=listenkb).start()
threading.Thread(target=draw).start()
while flag:
    data = s.recv(200).split(",")
    if len(data)==22:
        d=map(int,data[0:14])
        t=time.time()-tm
        data.append(t)
        b.append(map(float,data))
        cls=clf.predict([d])[0]
        print d,cls
        if cls==1 and oldstate!="1":
            s.send("fw")
            oldstate="1"
        elif cls==2 and oldstate!="2":
            s.send("rv")
            oldstate="2"
        elif cls==3 and oldstate!="3":
            s.send("rt")
            oldstate="3"
        elif cls==4 and oldstate!="4":
            s.send("lf")
            oldstate="4"
s.close()
