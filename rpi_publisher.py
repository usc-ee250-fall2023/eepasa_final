import sys
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
import grovepi
from grove_rgb_lcd import *
import paho.mqtt.client as mqtt
import time

########        ADD THIS FOR ENCRYPTION
from encrypt import Encrypt, Decrypt

key = b'12345678909876543212345678909876'
iv = b'1234567890987654'
###########

grovepi.pinMode(0, "INPUT") #light sensor port 0
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()

    while True:
        try:
            # get the distance from ultrasonic sensor and print it
            dist = grovepi.ultrasonicRead(4)
            displ = (str(dist) + "cm")

            ### ENCRYPTION
            encrypted_message = Encrypt(displ, key, iv)
            #rpi publishes ultrasonic ranger data for vm
            client.publish("pi/ultrasonicRanger", encrypted_message)
            #######

            # get the brightness from the light sensor
            brightness = grovepi.analogRead(0)

            #### ENCRYPTION
            encrypted_message = Encrypt(brightness, key,iv)
            #rpi publishes light sensor data for vm
            client.publish("pi/light", encrypted_message)
            ########

            # if the light turns on or if someone comes nearby, the warning is "Someone is coming!"
            if (brightness > 100 or dist < 50):
                ###### ENCRYPTION
                encrypted_message = Encrypt("Someone is coming!", key,iv)
                ##############
                client.publish("pi/warning", encrypted_message)
                # wait to see if they leave before sending another warning
                time.sleep(5)
            # if nothing is triggered, message is "Safe"
            else:
                ####### ENCRYPTION
                encrypted_message = Encrypt("Safe", key,iv)
                #########
                client.publish("pi/warning", encrypted_message)
            
        except IOError:
            print("error")

        time.sleep(1)
            
