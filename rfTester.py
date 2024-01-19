import rfdevice
import config
import time


def sendRF(Light, Stat):
    Left = [2328388096, 2194170368]
    Right = [2731041280, 2898813440]
    Main = [2462605824, 2630377984]
    if Light == "Left":
        sender.tx_code(int(Left[Stat]), int(2), int(707))
        sender.tx_code(int(Left[Stat]), int(2), int(710))
    if Light == "Right":
        sender.tx_code(int(Right[Stat]), int(2), int(707))
        sender.tx_code(int(Right[Stat]), int(2), int(710))
    if Light == "Main":
        sender.tx_code(int(Main[Stat]), int(2), int(707))
        sender.tx_code(int(Main[Stat]), int(2), int(710))
    print(Light, Stat)

sender = rfdevice.RFDevice()
sender.enable_tx()


light = input("Enter Light")
stat = int(input("Enter stat"))

sendRF(light, stat)
