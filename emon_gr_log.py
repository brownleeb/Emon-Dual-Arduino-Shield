#!/usr/bin/python2
import serial, time, datetime
import syslog
device_path="/dev/serial/by-id/"
emon_arduino1=device_path+"usb-Arduino__www.arduino.cc__0043_854393133303517010B1-if00"
emon_arduino=device_path+"usb-Arduino_LLC_Arduino_Leonardo-if00"
one_min=0
#
class RingBuffer(object):
    """ class that implements a not-yet-full buffer """
    def __init__(self, size_max):
        self.max = size_max
        self.data = [  ]
    class __Full(object):
        """ class that implements a full buffer """
        def append(self, x):
            """ Append an element overwriting the oldest one. """
            self.data[self.cur] = x
            self.cur = (self.cur+1) % self.max
        def tolist(self):
            """ return list of elements in correct order. """
            return self.data[self.cur:] + self.data[:self.cur]
    def append(self, x):
        """ append an element at the end of the buffer. """
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0
            # Permanently change self's class from non-full to full
            self.__class__ = self.__Full
    def tolist(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data

while 1:
   syslog.syslog("PyEmon - Initializing...")
   watts=0.0
   ser=serial.Serial(emon_arduino, 9600)
   ser1=serial.Serial(emon_arduino1, 9600)
   time.sleep(10)
   avg_watts=RingBuffer(60)
   now=datetime.datetime.now()
   f=open('/user1/power/logs/'+now.strftime("%Y-%m-%d")+".csv",'w')
   f.write("Time,Real Power Watts (last 30 sec),Apparent Power Watts (last 30 sec), Avg Power Factor, Avg Volts (RMS), Avg Current (RMS), # of Samples\n")
   f.close()
   while 1:
      try:
         while 1:
            try:
              temp=ser.readline()
              temp1=ser1.readline()
              if now.day != datetime.datetime.now().day:
                 now=datetime.datetime.now()
                 f=open('/user1/power/logs/'+now.strftime("%Y-%m-%d")+".csv",'w')
                 f.write("Time,Real Power Watts (last 30 sec),Apparent Power Watts (last 30 sec), Avg Power Factor, Avg Volts (RMS), Avg Current (RMS), # of Samples,  Temp\n")
                 f.close()
              f=open('/user1/power/logs/'+now.strftime("%Y-%m-%d")+".csv",'a')
              f.write(str(datetime.datetime.now())+','+temp.strip()+',1\n')
              f.write(str(datetime.datetime.now())+','+temp1.strip()+',2\n')
              f.close()
              atemp=temp.strip().split(',')
              atemp1=temp1.strip().split(',')
              f=open("/run/emon-temp",'w')
              f.write(atemp[6])
              f.close()
              watts=float(atemp[0])
              watts1=float(atemp1[0])
              watts=watts+watts1
              itemp=int(watts*1000)
              if (watts>0.0) and (watts<150.0):
                 f=open('/user1/power/power13.temp')
                 val=f.readline()
                 f.close()
                 f=open('/user1/power/power13.temp','w')
                 val=str(itemp+int(val))
                 f.write(val)
                 f.close()
                 f=open('/user1/power/power13.txt','w')
                 f.write(val[:-3])
                 f.close()
                 if one_min == 0:
                    one_min=watts
                 else:
                    OneMinRate=one_min+watts
                    one_min=0
                    avg_watts.append(OneMinRate)
                    temp_list=avg_watts.tolist()
                    OneMinRate=(OneMinRate * 60)/1000.0
                    FiveMinRate=(sum(temp_list[-5:])*12)/1000.0
                    HourRate=sum(temp_list)/1000.0
                    f=open('/dev/shm/power13.hist','w')
                    temp_str="%8.2f,%8.2f,%8.2f"%(OneMinRate,FiveMinRate,HourRate)
                    f.write(temp_str.replace(" ",""))
                    f.close()
              else:
                 syslog.syslog("PyEmon - Value out of range: "+temp)
              break
            except ValueError:
              syslog.syslog("PyEmon - ValueError: "+temp)
              time.sleep(10)
         time.sleep(10)
      except serial.serialutil.SerialException:
         syslog.syslog("PyEmon - Lost serial contact")
         ser.close()
         time.sleep(10)
         break
