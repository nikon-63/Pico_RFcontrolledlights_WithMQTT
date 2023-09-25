# Pico RF Controlled Lights With MQTT

This mini project lets you control remote control plug sockets with your iPhone. The plug sockets normally communicate with their remote over 433MHz, but you can use a Raspberry Pi Pico with an RF module to recode the signals sent from the remote.

I wrote a script that transmits the recoded signals from the Pico when it receives a message over MQTT to turn off or on the sockets. Homebridge publishes to the MQTT topic, providing an easy way to interface with the Pico from the Home app on iOS devices.    

Overall, this project provides a simple and effective way to control remote control plug sockets with your iPhone. It’s a great way to add smart home functionality to your home.