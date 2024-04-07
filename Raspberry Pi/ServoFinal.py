from re import T
import time
import subprocess
import paho.mqtt.client as paho
from paho import mqtt
import RPi.GPIO as GPIO
message_received = 5
ctr=[0,1,2,3,4] # 0-Up 1-Down  2-Right  3-Left 4-Default
Dir=4 ## IMPLEMENT LISTENER CODE FOR THIS VARIABLE

VservoPIN = 2
HservoPIN = 3
BuzzPIN=21
Vservo= 12
Hservo= 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(VservoPIN, GPIO.OUT)
GPIO.setup(HservoPIN, GPIO.OUT)
GPIO.setup(BuzzPIN, GPIO.OUT)


Vp = GPIO.PWM(VservoPIN, 50) # GPIO 2 for PWM with 50Hz
Hp = GPIO.PWM(HservoPIN, 50) # GPIO 3 for PWM with 50Hz

# Initialization
GPIO.output(BuzzPIN,GPIO.LOW)

def Initalize():
   Hp.start(Hservo)
   time.sleep(0.5)
   Hp.ChangeDutyCycle(0)
   time.sleep(0.5)
   Vp.start (Vservo)
   time.sleep(0.5)
   Vp.ChangeDutyCycle(0)
   time.sleep(0.5)
Initalize()
# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    global message_received
    message_received=str(msg.payload.decode("utf-8"))
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if (msg.topic=="Mobile/detect"):
        if(message_received=="7"):
             print("Alarm")
             GPIO.output(BuzzPIN,GPIO.HIGH)
    if (msg.topic=="Mobile/Arm"):
        if(message_received=="0"):
             print("Disarmed")
             GPIO.output(BuzzPIN,GPIO.LOW)
             message_received= 5

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("Camera", "Secura123")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("c4d8488a2a0544759c5c7696e88f744d.s1.eu.hivemq.cloud",8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("Mobile/Camera", qos=1)
client.subscribe("Mobile/detect", qos=1)
client.subscribe("Mobile/Arm", qos=1)

# a single publish, this can also be done in loops, etc.
IP=subprocess.run(['hostname', '-I'], capture_output=True)
IP= (IP.stdout.decode().strip())
print(IP)
client.publish("Mobile/IP", payload=("http://"+IP+":8080/stream"), qos=1,retain=True)


# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
#!/usr/bin/python




# setServoPulse(2,2500)
print("Enter Directtion")



client.loop_start()


try:
    while(True):
        Dir = message_received
        #print(Dir)
        if (Dir == '0'): #UP
            while(Dir == '0'):
                Dir = message_received
                if(Vservo<=7):
                    Vp.ChangeDutyCycle(0)
                    time.sleep(0.15)
                    break
                else:
                    Vservo -=0.5
                    Vp.ChangeDutyCycle(Vservo)
                    time.sleep(0.1)

        elif (Dir == '1'): #DOWN
            while(Dir == '1'):
                Dir = message_received
                if(Vservo>=12):
                    Vp.ChangeDutyCycle(0)
                    time.sleep(0.15)
                    break
                else:
                    Vservo +=0.5
                    Vp.ChangeDutyCycle(Vservo)
                    time.sleep(0.1)

        elif (Dir == '2'): #RIGHT
            while(Dir == '2'):
                Dir = message_received
                if(Hservo<=3):
                    Hp.ChangeDutyCycle(0)
                    time.sleep(0.15)
                    break
                else:
                    Hservo-= 0.5
                    Hp.ChangeDutyCycle(Hservo)
                    time.sleep(0.1)
        elif (Dir == '3'): #LEFT
            while(Dir == '3'):
                Dir = message_received
                if(Hservo>=10.5):
                    Hp.ChangeDutyCycle(0)
                    time.sleep(0.15)
                    break
                else:
                    Hservo+= 0.5
                    Hp.ChangeDutyCycle(Hservo)
                    time.sleep(0.1)

        elif (Dir == '4'): #DEFAULT
            #Hp.ChangeDutyCycle(7)
            #time.sleep(0.1)
            #Vp.ChangeDutyCycle(12)
            #time.sleep(0.1)
            #Hp.ChangeDutyCycle(0)
            #time.sleep(0.05)
            #Vp.ChangeDutyCycle(0)
            Initalize()
            Vservo= 12
            Hservo= 7

except:
    print ("\nProgram end")
    exit()
