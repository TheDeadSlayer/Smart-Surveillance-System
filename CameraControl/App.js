import React, { useState, useEffect, useRef } from 'react';
import { View, Button, StyleSheet, Image,TouchableOpacity, Text, Alert, Platform,SafeAreaView , AppRegistry } from 'react-native';
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import Constants from 'expo-constants';
import { WebView } from 'react-native-webview';
import  {AsyncStorage}  from '@react-native-async-storage/async-storage';
import init from 'react_native_mqtt';

init({
  size: 10000,
  storageBackend: AsyncStorage,
  defaultExpires: 1000 * 3600 * 24,
  enableCache: true,
  reconnect: true,
  sync : {
  }
});

async function registerForPushNotificationsAsync() {
  let token;
  if (Device.isDevice) {
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;
    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }
    if (finalStatus !== 'granted') {
      Alert.alert('Failed to get push token for push notification!');
      return;
    }
    // Use Constants.expoConfig to obtain the projectId
    const projectId = Constants.expoConfig.extra?.projectId;
    if (!projectId) {
      console.error('Project ID is undefined. Please make sure you have set it in your app.json or app.config.js.');
      return;
    }
    token = (await Notifications.getExpoPushTokenAsync({
      experienceId: projectId,
    })).data;
  } else {
    Alert.alert('Must use a physical device for Push Notifications');
  }

  if (Platform.OS === 'android') {
    Notifications.setNotificationChannelAsync('default', {
      name: 'default',
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: '#FF231F7C',
    });
  }

  Notifications.setNotificationHandler({
    handleNotification: async () => ({
      shouldShowAlert: true,
      shouldPlaySound: true,
      shouldSetBadge: false,
    }),
  });

  return token;
}

const DirectionButton = ({ source, onPress }) => (
  <TouchableOpacity onPress={onPress} style={styles.directionButton}>
    <Image source={source} style={styles.arrowIcon} resizeMode="contain" />
  </TouchableOpacity>
);

// The main component
const CameraControlApp = () => {
  const [expoPushToken, setExpoPushToken] = useState('');
  const notificationListener = useRef();
  const responseListener = useRef();
  const [streamUrl, setStreamUrl] = useState('');
  const client = new Paho.MQTT.Client('c4d8488a2a0544759c5c7696e88f744d.s1.eu.hivemq.cloud',8884,"MobileAPP123" + String(parseInt(Math.random)*100,100))
  



  useEffect(() => {
//  if (client && client.isConnected()) {
//       client.disconnect()
//     }
  
  client.connect({
  useSSL: true,
  reconnect: true,
  timeout: 3,
  onFailure: (e) => {
    console.log("Connection Failed")
    alert("Failed to connect to MQTT broker");
    client.reconnect()
  },
  userName: "Camera",
  password: "Secura123",
  onSuccess: () => {
    console.log("Connection Successful")
    client.subscribe("Mobile/IP", 1);
    client.subscribe("Mobile/detect", 1);
    client.reconnect()
    
  },
});

client.onMessageArrived = (message) => {
   
  const Dest= message._getDestinationName()
  console.log(message._getDestinationName())
  if (Dest =="Mobile/IP") {
     setStreamUrl(message._getPayloadString())
  }
  else if (Dest == "Mobile/detect") {
    if (message._getPayloadString() =="7"){
      console.log("Detect Here")
      handleArmPress()
    }
  }
};

  }, []);

  // useEffect(() => {
  //   client.reconnect()
  //      } )


  useEffect(() => {
    registerForPushNotificationsAsync().then(token => setExpoPushToken(token));

    notificationListener.current = Notifications.addNotificationReceivedListener(notification => {
      console.log(notification);
    });

    responseListener.current = Notifications.addNotificationResponseReceivedListener(response => {
      console.log(response);
    });

    return () => {
      Notifications.removeNotificationSubscription(notificationListener.current);
      Notifications.removeNotificationSubscription(responseListener.current);
    };
  }, []);

  const handleArmPress = async () => {
    await Notifications.scheduleNotificationAsync({
      content: {
        title: "Intruder Detected!!!",
        body: "An intruder has been detetced by the camera!!",
      },
      trigger: null,
    });
  };




  return (
    <SafeAreaView style={styles.container}>
      {/* Camera feed */}
      <WebView style={styles.cameraFeed} source={{ uri: streamUrl }} />
       {/* Reset Button
   <View style={styles.resetContainer}>
     <Button title="Reset" onPress={() => client.send("Mobile/Camera", "4", 1, true)} />
   </View> */}

      {/* Directional Arrows */}
      <View style={styles.directionalArrowsContainer}>
      <TouchableOpacity onPressIn={async() =>{ if (client && client.isConnected()) { client.send("Mobile/Camera", "0", 1, true)}}} onPressOut={() =>{ if (client && client.isConnected()) { client.send("Mobile/Camera", "5", 1, true)}}}>
        <Image source={require('./arrows/up.png')} style={styles.arrowIcon} />
      </TouchableOpacity>
      <View style={styles.horizontalArrows}>
      <TouchableOpacity onPressIn={async() =>{ if (client && client.isConnected()) { client.send("Mobile/Camera", "3", 1, true)}}} onPressOut={() =>{ if (client && client.isConnected()) { client.send("Mobile/Camera", "5", 1, true)}}}>
          <Image source={require('./arrows/left.png')} style={styles.arrowIcon} />
        </TouchableOpacity>
        <TouchableOpacity onPressIn={async() =>{ if (client && client.isConnected()) { client.send("Mobile/Camera", "2", 1, true)}}} onPressOut={() =>{ if (client && client.isConnected()) { client.send("Mobile/Camera", "5", 1, true)}}}>
          <Image source={require('./arrows/right.png')} style={styles.arrowIcon} />
        </TouchableOpacity>
      </View>
      <TouchableOpacity onPressIn={async ()=>{ if (client && client.isConnected()) { client.send("Mobile/Camera", "1", 1, true)}}} onPressOut={() =>{ if (client && client.isConnected()) { client.send("Mobile/Camera", "5", 1, true)}}}>
        <Image source={require('./arrows/down.png')} style={styles.arrowIcon} />
      </TouchableOpacity>
    </View>

      {/* Disarm and Arm Buttons */}
      <View style={styles.systemControl}>
        <Button title="Disarm" onPress={async() => client.send("Mobile/Arm", "0", 1, true)} />
        <Button title="Arm" onPress={async() => client.send("Mobile/Arm", "1", 1, true)} />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  cameraFeed: {
    width: '100%',
    aspectRatio: 4/ 3,
    marginTop: 40,
    marginLeft:0,
  },
  resetContainer: {
    alignItems: 'flex',
    flexDirection: 'row',
    marginVertical: 10,
    marginTop: 10,
    marginLeft:10,
  },
  directionalArrowsContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  horizontalArrows: {
    flexDirection: 'row',
    width: '60%', // Control the space between left and right arrows
    justifyContent: 'space-between',
  },
  directionButton: {
    padding: 20,
  },
  arrowIcon: {
    width: 50,
    height: 50,
  },
  systemControl: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 30,
    marginBottom: 20,
  },
});

export default CameraControlApp;