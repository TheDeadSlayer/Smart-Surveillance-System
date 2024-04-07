# Smart-Surveillance-System
# Overview
The Smart Surveillance System project leverages cutting-edge technologies including YOLO (You Only Look Once) Human Detection AI and IoT (Internet of Things) protocols to create a state-of-the-art surveillance system. Designed to process video streams in real-time directly at the network's edge, this system addresses the conventional challenges of latency and bandwidth in surveillance applications. At its core, it utilizes a modified YOLO model, enhanced with Residual Learning and Spatial Pyramid Pooling (SPP), ensuring efficient and accurate human detection.

# Features
Real-Time Human Detection: Uses an enhanced YOLO AI model for immediate identification of human figures in the video feed.
Edge Computing: Processes data at the edge of the network, reducing latency and bandwidth use.
IoT Integration: Facilitates remote management and scalability through IoT protocols.
Pan-Tilt Camera Control: Offers wide area coverage with motorized pan and tilt movements.
Low-Latency Video Streaming: Ensures swift data transmission for real-time surveillance applications.
Hardware and Software Requirements

# Hardware:
Raspberry Pi 3B (or higher)
Compatible Camera Module with night vision
Servo Motors for pan-tilt functionality
Additional sensors and actuators as needed for customization

# Software:
Python 3.6+
OpenCV library for computer vision tasks
Paho MQTT for messaging in IoT applications
Any MQTT broker (e.g., HiveMQ)
Node.js and npm for the server (optional)

# Installation
Provide step-by-step instructions on how to set up the project. This should include installing necessary libraries, setting up hardware, and running any initial configuration scripts.
#Seting up YoloV4 Humman Detection AI
1. Run pip3 install paho-mqtt
3. Download YoloV4.Weights : https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
4. Setup OpenCV to run on the Nvidia GPU by following this tutorial:https://www.youtube.com/watch?v=YsmhKar8oOc
5. Place YoloV4.weights in the Yolo folder

# Setting up MQTT Broker
1. Visit https://console.hivemq.cloud/
2. Create an Account or Sign in with Google
3. Create a cluster
4. Create copy the cluster URL and replace it in the App.js file in Camera Control folder, OpenCV.py in Yolo folder and ServoFinal.py in Raspberry Pi folder
5. Go back to HiveMQ and press on "Access Management"
6. Create a new credential (Username and Password)
7. Replace Username and Password in in the App.js file in Camera Control folder, OpenCV.py in Yolo folder and ServoFinal.py in Raspberry Pi folder

# Setting up Camera Streaming
1. Visit Camera Streamer Repo: https://github.com/ayufan/camera-streamer
2. Follow Instruction and Install Camera Streamer Server on Raspberry Pi
3. Run cd camera-streamer/
4. Run  tools/libcamera_camera.sh -camera-format=YUYV

# Setting up Hardware control script on Raspberry Pi
1. Run pip3 install paho-mqtt
2. Make sure hardware Pins are setup correctly in ServoFinal.py file in Raspberry Pi folder

# Setting up Mobile Application
1. Run npx expo start -c
2. Connect Android Mobile
3. Enable USB Debugging on Android Mobile
4. Press "a" in Terminal
5. Press "r" in Terminal

# Run the System
1. Run Camera Streamer by running cd camera-streamer/ then running tools/libcamera_camera.sh -camera-format=YUYV
2. Run python3 ServoFinal.py
3. Run OpenCV.py script on computer
4. Follow Steps to Rin Mobile Application
   
