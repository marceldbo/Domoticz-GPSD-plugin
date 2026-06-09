# Domoticz-GPSD-plugin

The idea of this plugin started when I made a small Raspberry Pi HAT with a GPS Module from one of the Chinese Warehouses. The initial goal of the GPS HAT was to serve accurate time to my home network using gpsd and chrony. This works perfectly, however I was missing a simple dashboard to view the status information of the gpsd daemon. Together with Chatgpt I created a plugin for Domoticz that, once installed, creates a domoticz text device, and polls the gpsd.socket 2947 every 30 seconds, and presents the most relevant data to this device.

# Installation

Create a new directory in '/home/pi/domoticz/plugins', e.g. gpsd, and place the 'plugin.py' file in this directory. Make the file executable: 'sudo chmod 755 plugin.py'. Now stop and start the domoticz service. The plugin should be selectable under the 'Hardware tab'. Before configuring, make sure that Domoticz accepts new devices. Configure the plugin. A new GPS device should be available under the 'Devices tab'.

For convenience, I have also created an icon to be used with the newly created device. This can be installed by uploading the 'Gpsd.zip' file to the custom icons section in the Domoticz GUI and updating the device.
