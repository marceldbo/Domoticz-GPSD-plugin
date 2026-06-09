#
# Domoticz GPSD plugin
#
# Author: Marcel de Bont using OpenAI
#
# Creation date: June 9, 2026
#
# Revision: 2.0.0
#
"""
<plugin key="GPSD_STAT" name="GPSD Status Monitor" author="Marcel de Bont & OpenAI" version="2.0.0" wikilink="" externallink="https://github.com/marceldbo/Domoticz-GPSD-Plugin.git">
    <description>
        GPSD plugin for Domoticz with stable streaming and correct satellite handling.
    </description>
    <params>
        <param field="Address" label="GPSD Host" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="GPSD Port" width="75px" required="true" default="2947"/>
        <param field="Mode1" label="Update Interval (sec)" width="75px" required="false" default="30"/>
    </params>
</plugin>
"""

import Domoticz
import socket
import json
import time
import threading

class BasePlugin:

    def __init__(self):
        self.next_update = 0
        self.sock = None
        self.buffer = ""
        self.tpv = None
        self.sats_used = 0
        self.sats_visible = 0

    # --------------------------------------------------
    # START
    # --------------------------------------------------
    def onStart(self):

        Domoticz.Log("GPSD plugin started")

        if 1 not in Devices:
            Domoticz.Device(
                Name="GPSD Status",
                Unit=1,
                TypeName="Text"
            ).Create()

        Domoticz.Heartbeat(10)

        self.connect()

    # --------------------------------------------------
    # CONNECT TO GPSD
    # --------------------------------------------------
    def connect(self):

        try:
            host = Parameters.get("Address", "127.0.0.1")
            port = int(Parameters.get("Port", "2947") or 2947)

            Domoticz.Log(f"Connecting to GPSD {host}:{port}")

            self.sock = socket.create_connection((host, port), timeout=5)
            self.sock.settimeout(1.0)

            self.sock.recv(4096)
            self.sock.sendall(b'?WATCH={"enable":true,"json":true};\n')

        except Exception as e:
            Domoticz.Error(f"GPSD connect failed: {e}")
            self.sock = None

    # --------------------------------------------------
    # HEARTBEAT
    # --------------------------------------------------
    def onHeartbeat(self):

        interval = 30
        try:
            raw = Parameters.get("Mode1", "")
            if raw and str(raw).strip().isdigit():
                interval = int(raw)
        except:
            interval = 30

        if time.time() < self.next_update:
            return

        self.next_update = time.time() + interval

        self.poll_gpsd()

        if self.tpv:
            text = self.format_status()

            if 1 in Devices:
                Devices[1].Update(
                    nValue=0,
                    sValue=text
                )

    # --------------------------------------------------
    # READ GPSD STREAM (NON-BLOCKING)
    # --------------------------------------------------
    def poll_gpsd(self):

        if not self.sock:
            self.connect()
            return

        try:
            data = self.sock.recv(4096).decode("utf-8", errors="ignore")
            self.buffer += data

            while "\n" in self.buffer:
                line, self.buffer = self.buffer.split("\n", 1)

                try:
                    obj = json.loads(line)
                except:
                    continue

                cls = obj.get("class")

                # POSITION FIX
                if cls == "TPV":
                    self.tpv = obj

                # SATELLITES
                elif cls == "SKY":
                    sats = obj.get("satellites", [])

                    self.sats_used = sum(
                        1 for s in sats if s.get("used", False)
                    )

                    self.sats_visible = len(sats)

        except socket.timeout:
            pass

        except Exception as e:
            Domoticz.Error(f"GPSD read error: {e}")
            self.sock = None

    # --------------------------------------------------
    # FORMAT OUTPUT
    # --------------------------------------------------
    def format_status(self):

        mode = self.tpv.get("mode", 0)

        fix = {
            0: "Unknown",
            1: "None",
            2: "2D",
            3: "3D"
        }.get(mode, "Unknown")

        return (
            "Fix: {}, Sats (Used/Seen): {}/{}, Alt: {} m\n"
            "Lat: {}, Lon: {}\n"
#            "Time: {}"
        ).format(
            fix,
            self.sats_used,
            self.sats_visible,
            self.tpv.get("alt", "N/A"),
            self.tpv.get("lat", "N/A"),
            self.tpv.get("lon", "N/A"),
#            self.tpv.get("time, "N/A")
        )


global _plugin
_plugin = BasePlugin()

def onStart():
    _plugin.onStart()

def onHeartbeat():
    _plugin.onHeartbeat()
