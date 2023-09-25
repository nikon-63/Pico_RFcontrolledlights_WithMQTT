import rfdevice
import config
import time

receiver = rfdevice.RFDevice()
receiver.enable_rx()


timestamp = None

while True:
    if receiver.rx_code_timestamp != timestamp:
        timestamp = receiver.rx_code_timestamp
        if timestamp != None:
            print('{ "code": "' + str(receiver.rx_code) + '", "pulselength": "' + str(receiver.rx_pulselength) + '", "protocol": "' + str(receiver.rx_proto) + '" }')
        time.sleep(1)
