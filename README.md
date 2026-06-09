# Domoticz-GPSD-plugin

The idea of this plugin started when I made a small Raspberry Pi HAT with a GPS Module from one of the Chinese Warehouses. The initial goal of the GPS HAT was to serve accurate time to my home network using gpsd and chrony. This works perfectly, however I was missing a simple dashboard to view the status information of the gpsd daemon. Together with Chatgpt I created a plugin for Domoticz that, once installed, creates a domoticz text device, and polls the gpsd.socket 2947 every 30 seconds, and presents the most relevant data to this device.
