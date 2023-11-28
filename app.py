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
    if msg.topic == "kackar/web_dist":
        sensor_data["distance"] = str(msg.payload, "utf-8")
    if msg.topic == "kackar/web_light":
        sensor_data["brightness"] = str(msg.payload, "utf-8")
    index()
    
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
client.connect("test.mosquitto.org", 1883, 60)
client.subscribe("kackar/data")
client.subscribe("kackar/web_dist")
client.subscribe("kackar/web_light")
client.loop_start()

# Define the route to display sensor data
@app.route('/')
def index():
    return render_template('index.html', sensor_data = sensor_data)

if __name__ == '__main__':
    app.run(debug=True)
