import machine
import ubinascii
import time
import network
from mqtt.simple import MQTTClient
from machine import Pin
import rfdevice
import config

WIFI_SSID = ''
WIFI_PASSWORD = ''
MQTT_BROKER = ''
MQTT_USER = ''
MQTT_PASSWORD = ''
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPICS = [b"MainBedLights/Right/Set", b"MainBedLights/Left/Set", b"MainBedLights/Main/Set"]

# RF code
Left = [2328388096, 2194170368]
Right = [2731041280, 2898813440]
Main = [2462605824, 2630377984]
sender = rfdevice.RFDevice()
sender.enable_tx()


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        wlan.ifconfig(('192.168.100.41', '255.255.255.0', '192.168.100.1', '8.8.8.8'))
        while not wlan.isconnected():
            pass
    print('Network Config:', wlan.ifconfig())


def mqtt_callback(topic, msg):
    if topic == b"MainBedLights/Right/Set":
        if msg == b"0":
            sender.tx_code(int(Right[0]), int(2), int(707))
            sender.tx_code(int(Right[0]), int(2), int(710))
            print('Right light turned OFF')
        elif msg == b"1":
            sender.tx_code(int(Right[1]), int(2), int(707))
            sender.tx_code(int(Right[1]), int(2), int(710))
            print('Right light turned ON')
            
    elif topic == b"MainBedLights/Left/Set":
        if msg == b"0":
            sender.tx_code(int(Left[0]), int(2), int(707))
            sender.tx_code(int(Left[0]), int(2), int(710))
            print('Left light turned OFF')
        elif msg == b"1":
            sender.tx_code(int(Left[1]), int(2), int(707))
            sender.tx_code(int(Left[1]), int(2), int(710))
            print('Left light turned ON')
            
    elif topic == b"MainBedLights/Main/Set":
        if msg == b"0":
            sender.tx_code(int(Main[0]), int(2), int(707))
            sender.tx_code(int(Main[0]), int(2), int(710))
            print('Main light turned OFF')
        elif msg == b"1":
            sender.tx_code(int(Main[1]), int(2), int(707))
            sender.tx_code(int(Main[1]), int(2), int(710))
            print('Main light turned ON')


def connect_mqtt():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
    client.set_callback(mqtt_callback)
    client.connect()
    print('Connected to %s MQTT broker' % MQTT_BROKER)
    return client


def main():
    led = Pin('LED', Pin.OUT)
    led.off()
    connect_wifi(WIFI_SSID, WIFI_PASSWORD)
    client = connect_mqtt()
    led.on()
    for topic in TOPICS:
        client.subscribe(topic)
        print('Subscribed %s Topic' % topic.decode())

    try:
        while True:
            client.wait_msg()
    except OSError as e:
        print('Reading Error: Reconnecting...')
        led.off()
        time.sleep(5.0)
        machine.reset()

if __name__ == "__main__":
    main()


