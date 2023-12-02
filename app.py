from flask import Flask, render_template
import json
import paho.mqtt.client as mqtt
from encrypt import Encrypt, Decrypt
key = b'12345678909876543212345678909876'
iv = b'1234567890987654'
app = Flask(__name__)

# Store the latest sensor data

def on_message(client, userdata, msg):
   # set correct variable to data received
    if msg.topic == "kackar/web_dist":
        sensor_data["distance"] = str(msg.payload, "utf-8")
    if msg.topic == "kackar/web_light":
        sensor_data["brightness"] = str(msg.payload, "utf-8")

sensor_data = {"distance": "N/A", "brightness": "N/A"}

def dist_callback(client, userdata, msg):
        # decrypt the data to get the distance in cm
        decrypt_msg = Decrypt(msg.payload.decode(), key, iv)
        #print(f"dist: {decrypt_msg} cm")
        sensor_data["distance"] = str(msg.payload, "utf-8")

def light_callback(client, userdata, msg):
        # decrypt the data to get the brightness level
        decrypt_msg = Decrypt(msg.payload.decode(), key, iv)
        #print(f"brightness: {decrypt_msg}")
        sensor_data["brightness"] = str(msg.payload, "utf-8")
    
# Set up the MQTT client
client = mqtt.Client()
client.on_message = on_message
client.connect("test.mosquitto.org", 1883, 60)
#client.subscribe("kackar/data")
client.subscribe("kackar/web_dist")
#client.message_callback_add("kackar/web_dist", dist_callback)
client.subscribe("kackar/web_light")
#client.message_callback_add("kackar/web_dist", light_callback)
client.loop_start()

# Define the route to display sensor data
@app.route('/')
def index():
    return render_template('index.html', sensor_data = sensor_data)

if __name__ == '__main__':
    app.run(debug=True)
