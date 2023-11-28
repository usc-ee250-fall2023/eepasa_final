"""EE 250L Lab 04 Starter Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from text import text

###### Decryption
from encrypt import Encrypt, Decrypt


key = b'12345678909876543212345678909876'
iv = b'1234567890987654'
######


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    global count
    count = 0
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

#####  ALL CALLBACKS HAVE DECRYPT
###### SHOULD DISPLAY ENCRYPTED AND DECRYPTED MSG

def dist_callback(client, userdata, msg):

    decrypt_msg = Decrypt(msg.payload.decode(), key, iv)
    encrypt_msg = msg.payload.decode()
    client.publish("kackar/web_dist", decrypt_msg)

    print(encrypt_msg)
    
def light_callback(client, userdata, msg):

    decrypt_msg = Decrypt(msg.payload.decode(), key, iv)
    encrypt_msg = msg.payload.decode()
    client.publish("kackar/web_light", decrypt_msg)
    print(encrypt_msg)


def warning_callback(client, userdata, msg):

    global count
    
    encrypt_msg = msg.payload.decode()
    decrypt_msg = Decrypt(encrypt_msg, key, iv)
    print(encrypt_msg)

    if (decrypt_msg == "Someone is coming!" and count%10 == 0):
        text(decrypt_msg)
    elif decrypt_msg == "Safe":
        count = 0
    else:
        count += 1
        
"""
    if decrypt_msg == "Someone is coming!":
        text(decrypt_msg)
        time.sleep(30)
"""
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
