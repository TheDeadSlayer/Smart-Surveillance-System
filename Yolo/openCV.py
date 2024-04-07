import numpy as np
import cv2
import time
import json
import os
import sys
import paho.mqtt.client as paho
from paho import mqtt

message_received=100
armed="0"
IP=""
disarmFlag=0


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
    global armed
    global IP
    message_received=str(msg.payload.decode("utf-8"))
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if (msg.topic=="Mobile/Arm"):
        armed= message_received
        print ("Armed= ",armed)
    if (msg.topic=="Mobile/IP"):
        IP= message_received
        print (IP)


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
client.subscribe("Mobile/Arm", qos=1)
client.subscribe("Mobile/IP", qos=1)
# a single publish, this can also be done in loops, etc.

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
#!/usr/bin/python
client.publish("Mobile/detect", payload=("6"), qos=1,retain=True)
client.loop_start()

net=cv2.dnn.readNet('C:\\Users\\shahw\\Desktop\\Yolo\\yolov4.weights','C:\\Users\\shahw\\Desktop\\Yolo\\\yolov4.cfg')


classes = []
with open("C:\\Users\\shahw\\Desktop\\Yolo\\\coco.names","r") as f:
    classes = [line.strip() for line in f.readlines()]


layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

colors= np.random.uniform(0,255,size=(len(classes),3))

# #print(IP)
# cap = cv2.VideoCapture(IP)
# #cap = cv2.VideoCapture("http://192.168.2.203:8080/stream")
# font = cv2.FONT_HERSHEY_PLAIN
# starting_time= time.time()
# frame_id = 0
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

while True:
    if(IP !=""):
        cap = cv2.VideoCapture(IP)
        #cap = cv2.VideoCapture("http://192.168.2.203:8080/stream")
        font = cv2.FONT_HERSHEY_PLAIN
        starting_time= time.time()
        frame_id = 0
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        try:
            while True:
                armed=message_received
                if armed=="0":
                    disarmFlag=0
                    
                _,frame= cap.read()  
                frame_id+=1

                height,width,channels = frame.shape
                blob = cv2.dnn.blobFromImage(frame,0.00392,(320,320),(0,0,0),True,crop=False)   

                net.setInput(blob)
                outs = net.forward(output_layers)

                class_ids=[]
                confidences=[]
                boxes=[]
                for out in outs:
                    for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence > 0.3:
                            center_x= int(detection[0]*width)
                            center_y= int(detection[1]*height)
                            w = int(detection[2]*width)
                            h = int(detection[3]*height)
                            x=int(center_x - w/2)
                            y=int(center_y - h/2)

                            boxes.append([x,y,w,h])
                            confidences.append(float(confidence)) 
                            class_ids.append(class_id) 

                indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6)

                for i in range(len(boxes)):
                    if i in indexes:
                        x,y,w,h = boxes[i]
                        label = str(classes[class_ids[i]])
                        confidence= confidences[i]
                        color = colors[class_ids[i]]
                        if(label=='person'):
                            if(confidence>0.5 and armed=="1" and disarmFlag==0):
                                    client.publish("Mobile/detect", payload=("7"), qos=1)
                                    print ("Intruder Detected")
                                    disarmFlag=1
                            cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
                            cv2.putText(frame,label+" "+str(round(confidence,2)),(x,y+30),font,1,(255,255,255),2)
                        
                elapsed_time = time.time() - starting_time
                fps=frame_id/elapsed_time
                cv2.putText(frame,"FPS:"+str(round(fps,2)),(10,50),font,2,(0,0,0),1)

                cv2.imshow("Image",frame)
                key = cv2.waitKey(1)

                if key == 27: 
                    break;

        except KeyboardInterrupt:
            print("done")
            
        cap.release()    
        cv2.destroyAllWindows()   