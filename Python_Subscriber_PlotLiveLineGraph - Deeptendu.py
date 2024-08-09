import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re

broker = "test.mosquitto.org"
topic = "yts2024/wise/grp12"
humvals = []
tempvals = []
ppmvals = []
rpmvals = []

fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=(10, 10))
plt.subplots_adjust(hspace=0.5)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(topic)
    else:
        print("Connection failed")

def on_message(client, userdata, msg):
    global humvals, tempvals, ppmvals, rpmvals
    message = msg.payload.decode()
    
    if message.startswith("humidity"):
        hum = float(message[message.find(":")+1:])
        humvals.append(hum)
    if message.startswith("Temperature"):
        temp = float(message[message.find(":")+1:])
        tempvals.append(temp)
    if message.startswith("RPM"):
        rpm = float(message[message.find(":")+1:])
        rpmvals.append(rpm)
    if message.startswith("MQ135 value"):
        ppm = float(message[message.find(":")+1:])
        ppmvals.append(ppm)
    if message.startswith("magnet is stuck"):
        exit()

def update_plot(i):
    if len(humvals) == 0:
        print("No data to plot yet")
        return 
    
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    
    ax1.plot(humvals, label='Humidity', color='blue')
    ax1.legend()
    ax1.set_title('Humidity')
    ax1.set_ylabel('Humidity (%)')

    ax2.plot(tempvals, label='Temperature', color='red')
    ax2.legend()
    ax2.set_title('Temperature')
    ax2.set_ylabel('Temperature (°C)')

    ax3.plot(ppmvals, label='PPM', color='green')
    ax3.legend()
    ax3.set_title('PPM')
    ax3.set_ylabel('PPM')

    ax4.plot(rpmvals, label='RPM', color='purple')
    ax4.legend()
    ax4.set_title('RPM')
    ax4.set_ylabel('RPM')
    ax4.set_xlabel('Time')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, 1883, 60)
client.loop_start()

ani = animation.FuncAnimation(fig, update_plot, interval=2000, cache_frame_data=False)

try:
    def update_plot(i):
        if len(humvals) == 0:
            print("No data to plot yet")
            return 
        
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        
        ax1.plot(humvals, label='Humidity', color='blue')
        ax1.legend()
        ax1.set_title('Humidity')
        ax1.set_ylabel('Humidity (%)')

        ax2.plot(tempvals, label='Temperature', color='red')
        ax2.legend()
        ax2.set_title('Temperature')
        ax2.set_ylabel('Temperature (°C)')

        ax3.plot(ppmvals, label='PPM', color='green')
        ax3.legend()
        ax3.set_title('PPM')
        ax3.set_ylabel('PPM')

        ax4.plot(rpmvals, label='RPM', color='purple')
        ax4.legend()
        ax4.set_title('RPM')
        ax4.set_ylabel('RPM')
        ax4.set_xlabel('Time')

    plt.show()
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()