# Smart-Surveillance-System
#Seting up YoloV4 Humman Detection AI
1. Run pip3 install paho-mqtt
3. Download YoloV4.Weights : https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
4. Setup OpenCV to run on the Nvidia GPU by following this tutorial:https://www.youtube.com/watch?v=YsmhKar8oOc
5. Place YoloV4.weights in the Yolo folder

#Setting up MQTT Broker
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

#Setting up Hardware control script on Raspberry Pi
1. Run pip3 install paho-mqtt
2. Make sure hardware Pins are setup correctly in ServoFinal.py file in Raspberry Pi folder

#Setting up Mobile Application
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
   
