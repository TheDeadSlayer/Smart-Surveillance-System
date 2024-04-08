
# Smart Surveillance System

## [Project Demo Video Link]: (https://drive.google.com/file/d/1_oQn3kJ3bqXLPDXdv7g2rExZY7DbykNg/view?usp=sharing)

## Overview
The Smart Surveillance System is an integrated solution leveraging advanced AI, MQTT communication, and mobile technology to offer real-time monitoring and control. This guide will help you set up the system, including YoloV4 for human detection, MQTT for messaging, camera streaming, hardware controls on Raspberry Pi, and the mobile app.

## Prerequisites

- Python 3.x
- pip3
- Access to an Nvidia GPU (for YoloV4)
- Raspberry Pi setup for hardware controls

## Setup Instructions

### YoloV4 Human Detection AI

1. Install paho-mqtt with `pip3 install paho-mqtt`.
2. Download the YoloV4 weights from the [YoloV4 GitHub Release](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights).
3. Set up OpenCV to run on an Nvidia GPU by following [this video tutorial](https://www.youtube.com/watch?v=YsmhKar8oOc).
4. Place the `yolov4.weights` file in the Yolo folder within your project directory.

### Setting up MQTT Broker

1. Sign up or sign in at [HiveMQ Cloud](https://console.hivemq.cloud/).
2. Create a new cluster.
3. Note down your cluster URL and replace it in the `App.js` file in the Camera Control folder, `OpenCV.py` in the Yolo folder, and `ServoFinal.py` in the Raspberry Pi folder.
4. In HiveMQ, navigate to "Access Management" and create a new credential (Username and Password).
5. Update the `App.js`, `OpenCV.py`, and `ServoFinal.py` files with the new username and password.

### Setting up Camera Streaming

1. Clone the [Camera Streamer Repository](https://github.com/ayufan/camera-streamer) and follow the installation instructions for Raspberry Pi.
2. Navigate to the camera-streamer directory: `cd camera-streamer/`.
3. Execute `tools/libcamera_camera.sh -camera-format=YUYV` to start the camera streamer.

### Setting up Hardware Control Script on Raspberry Pi

1. Ensure `paho-mqtt` is installed with `pip3 install paho-mqtt`.
2. Verify that the hardware pins are correctly set up in the `ServoFinal.py` file in the Raspberry Pi folder.

### Setting up the Mobile Application

1. Start the Expo project with `npx expo start -c`.
2. Connect an Android device via USB.
3. Enable USB Debugging on your Android device.
4. In the terminal, press "a" to launch the app on your connected Android device.
5. Press "r" to reload the app if necessary.

### Running the System

1. Launch the camera streamer: Navigate to the camera-streamer directory and execute `tools/libcamera_camera.sh -camera-format=YUYV`.
2. Run `python3 ServoFinal.py` on the Raspberry Pi to initiate hardware control.
3. Execute `OpenCV.py` on your computer to start the YoloV4 human detection.
4. Follow the above steps to run the mobile application for remote monitoring and control.

