import paho.mqtt.client as mqtt
import json
from glcd12864_lib import GLCD12864
import time

# Initialize the LCD
lcd = GLCD12864()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker !")
    print(f"Connected with result code {rc}")
    client.subscribe("tele/tasmota_923BC8/SENSOR")  #put here your mqtt topic that you want to subscribe and see data

def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    decoded_message = str(msg.payload.decode("utf-8"))
    msg = json.loads(decoded_message)
    print(msg)

    Temperature = extract_key_value(msg, "Temperature")
    print("Temperature : ", Temperature, " C")
    Humidity = extract_key_value(msg, "Humidity")
    print("Humidity : ", Humidity, " %")

    # Update the LCD display
    lcd.initTextMode()
    lcd.clearText()
    lcd.printStringTextMode(f"Temp: {Temperature} C", 0, 0)
    lcd.printStringTextMode(f"Humidity: {Humidity} %", 0, 1)

def extract_key_value(data, key):
    # Check if the key is in the top level
    if key in data:
        return data[key]

    # Recursively search for the key in nested dictionaries
    for k, v in data.items():
        if isinstance(v, dict):
            item = extract_key_value(v, key)
            if item is not None:
                return item
    return None

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.100.159", 1883, 60)   # replace my ip with your ip of mosquito mqtt server running

try:
    client.loop_forever()
finally:
    lcd.cleanup()
