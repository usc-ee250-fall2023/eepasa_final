"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""
import sys
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
import grovepi
from grove_rgb_lcd import *

import paho.mqtt.client as mqtt
import time

########        ADD THIS FOR ENCRYPTION
from encrypt import Encrypt, Decrypt

key = b'12345678909876543212345678909876'
iv = b'1234567890987654'
###########

grovepi.pinMode(0, "INPUT") #light senspr A0 on grovepi
#grovepi.pinMode(3, "INPUT") #light sensor port 3
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
'''
    #rpi wants to receive reuqests on whether to turn led on or off
    client.subscribe("kackar/led") 
    #rpi wants to receive requests on what to print on lcd from keyboard
    client.subscribe("kackar/lcd")

    client.message_callback_add("kackar/led", led_callback)
    client.message_callback_add("kackar/lcd", lcd_callback)

def led_callback(client, userdata, msg):
    stR = msg.payload.decode()
    if stR == "LED_ON":
        grovepi.digitalWrite(2,1)

    elif stR == "LED_OFF":
        grovepi.digitalWrite(2, 0)
        
def lcd_callback(client, userdata, msg):
    lcd_print = msg.payload.decode()
    setText_norefresh(lcd_print)
'''


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
    #pinMode(2, OUTPUT)

    while True:
        try:
            dist = grovepi.ultrasonicRead(4)
            displ = (str(dist))

            ### ENCRYPTION
            encrypted_message = Encrypt(displ, key, iv)
            #rpi publishes ultrasonic Ranger data for vm
            client.publish("pi/ultrasonicRanger", encrypted_message)
            #######

            brightness = grovepi.analogRead(0)

            #### ENCRYPTION
            encrypted_message = Encrypt(brightness, key,iv)
            #rpi publishes light sensor data for vm
            client.publish("pi/light", encrypted_message)
            ########
            if (brightness > 100 or dist < 50):
                #rpi publishes whether someone is near

                ###### ENCRYPTION
                encrypted_message = Encrypt("Someone is coming!", key,iv)
                client.publish("pi/warning", encrypted_message)
                ##############
            """
            else:
                ####### ENCRYPTION
                encrypted_message = Encrypt("Safe", key,iv)
                client.publish("pi/warning", encrypted_message)
                #########
            """
        except IOError:
            print("error")

        time.sleep(1)
            
