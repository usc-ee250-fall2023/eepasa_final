"""EE 250L Lab 04 Starter Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from text import text

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #vm wants to receive requests from ultrasonic Ranger 
    #and light sensor to see if someone is passing by
    #and warning tells if someone is or isn't
    client.subscribe("pi/ultrasonicRanger")
    client.subscribe("pi/light")
    client.subscribe("pi/warning")
    client.message_callback_add("pi/ultrasonicRanger", dist_callback)
    client.message_callback_add("pi/light", light_callback)
    client.message_callback_add("pi/warning", warning_callback)

# custom callbacks
def dist_callback(client, userdata, msg):
    print("dist: " + msg.payload.decode() + " cm")
def light_callback(client, userdata, msg):
    print("brightness: " + msg.payload.decode())
def warning_callback(client, userdata, msg):
    print(msg.payload.decode())
    if msg.payload.decode() == "Someone is coming!":
        text.text()
        time.sleep(5)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))



if __name__ == '__main__':
    #set up connection
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host= "test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()

    while True:
       # print("delete this line")
        time.sleep(1)        
