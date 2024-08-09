import paho.mqtt.client as mqtt

broker = "test.mosquitto.org"
topic = "yts2024/wise/grp12"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(topic)
    else:
        print("Connection failed")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received message: {message}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, 1883, 60)
client.loop_start()