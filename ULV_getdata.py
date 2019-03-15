import time
from pynput.keyboard import Key,Listener
import socket
import threading
import pickle
import matplotlib.pyplot as plt
import math
def recvfun():
    global s,flag,a,status,prevstate,tm
    while flag:
        d = s.recv(200)
        dsplit=d.split(",")
        t=time.time()-tm
        if status==True and d.startswith("wait")!=True and state!=prevstate and len(dsplit)==22 and dsplit[0]!="":
            d=str(state)+","+d+","+str(t)
            a.append(d)
            prevstate=state
        if len(dsplit)==22 and d.startswith("wait")!=True and dsplit[0]!="" and status==True:
            dsplit.append(t)
            b.append(map(float,dsplit))
        print dsplit

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
def on_press(key):
    global oldstate,state,s,status,tm,b
    cmd=str(key)
    if(cmd=="u'w'" and oldstate!="w"):
        state=1
        print "forward"
        s.send("fw")
        oldstate="w"
    elif(cmd=="u's'" and oldstate!="s"):
        state=2
        print "reverse"
        s.send("rv")
        oldstate="s"
    elif(cmd=="u'd'" and oldstate!="d"):
        state=3
        print "right"
        s.send("rt")
        oldstate="d"
    elif(cmd=="u'a'" and oldstate!="a"):
        state=4
        print "left"
        s.send("lt")
        oldstate="a"
    elif(cmd=="u'e'"):
        status= not status
        if status:
            b=[]
            tm=time.time()
            print "storing training set"
        else:
            print "stoping storing training set"
    elif(cmd=="u'g'"):
        s.send("startd")
    elif(cmd=="u'h'"):
        s.send("stopd")
        

        
def on_release(key):
    global oldstate,state,s,flag
    if key == Key.esc:
        storedata()
        s.send("exit!!")
        flag=False
        s.close()
        return False
    if(oldstate!="stop"):
        print "stopped"
        s.send("stop")
        oldstate="stop"
    
def storedata():
    f=open("rawdata.pkl","wb")
    pickle.dump(a,f)
    f.close()
try:
    a=[]
    b=[]
    status=False
    flag=True
    prevstate=0
    oldstate=""
    state=0
    tm=0
    s=socket.socket()
    s.connect(("192.168.43.5",8000))
    threading.Thread(target=recvfun).start()
    threading.Thread(target=draw).start()
    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
except Exception as e:
    print e
    storedata()
            
        
        
