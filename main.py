import network
from mqtt.simple import MQTTClient
from machine import Pin
import rfdevice
import config
import time

led = Pin('LED', Pin.OUT)
led.off()


def sendRF(Light, Stat):
    # Off code then On code
    right = [2395496960, 2177393152]
    left = [2529714688, 2663932416]
    if Light == "Right":
        sender.tx_code(int(right[Stat]), int(2), int(710))
    if Light == "Left":
        sender.tx_code(int(left[Stat]), int(2), int(710))



def sub_cb(topic, msg):
    msg = msg.decode('utf-8')
    print(topic)
    if msg == "true":
        led.on()
        if topic == b'Bedsidelight/Right/Set':
            #Right bed side light on
            print("Right bed side light on")
            sendRF("Right", 0)
        if topic == b'Bedsidelight/Left/Set':
            #Left bed side light on
            sendRF("Left", 0)
            print("Left bed side light on")
    elif msg == "false":
        led.off()
        if topic == b'Bedsidelight/Right/Set':
            #Right bed side light off
            sendRF("Right", 1)
            print("Right bed side light off")
        if topic == b'Bedsidelight/Left/Set':
            #Left bed side light off
            sendRF("Left", 1)
            print("Left bed side light off")


#Connect WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("<Wifi SSID>","<WiFi Password>")
wlan.ifconfig(('192.168.100.41', '255.255.255.0', '192.168.100.1', '8.8.8.8'))
time.sleep(5)

#MQTT Settings and connection
mqtt_server = '<MQTT IP>'
client_id = 'PicoW'
user_t = '<MQTT USERNAME>'
password_t = '<MQTT PASSWORD>'
client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60)
client.set_callback(sub_cb)
client.connect()

sender = rfdevice.RFDevice()
sender.enable_tx()

while True:
    # The MQTT topics 
    client.subscribe("Bedsidelight/Right/Set")
    client.subscribe("Bedsidelight/Left/Set")
    time.sleep(1)

