from flask import Flask, render_template
import json
import paho.mqtt.client as mqtt
from encrypt import Encrypt, Decrypt
key = b'12345678909876543212345678909876'
iv = b'1234567890987654'
app = Flask(__name__)


# Store the latest sensor data
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #vm wants to receive requests from ultrasonic Ranger 
    #and light sensor to see if someone is passing by
    #and warning tells if someone is or isn't
    client.subscribe("kackar/web_light")
    client.subscribe("kackar/web_dist")
    client.message_callback_add("kackar/web_light", light_callback)
    client.message_callback_add("kackar/web_dist", dist_callback)

sensor_data = {"distance": "N/A", "brightness": "N/A"}


def dist_callback(client, userdata, msg):
        decrypt_msg = Decrypt(msg.payload.decode(), key, iv)
        decrypt_msg = str(decrypt_msg)
        sensor_data["distance"] = decrypt_msg
        print(f"dist: {decrypt_msg} cm")

def light_callback(client, userdata, msg):
        decrypt_msg = Decrypt(msg.payload.decode(), key, iv)
        decrypt_msg = str(decrypt_msg)
        sensor_data["brightness"] = decrypt_msg
        print(f"brightness: {decrypt_msg}")
    
# Set up the MQTT client
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host= "test.mosquitto.org", port=1883, keepalive=60)
client.loop_start()

# Define the route to display sensor data
@app.route('/')
def index():
    return render_template('index.html', sensor_data = sensor_data)

if __name__ == '__main__':
    app.run(debug=True)
