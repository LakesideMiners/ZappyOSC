#!/usr/bin/python
## Serial Port Logger Application
# I forgot where I got the basees for this, sorry!
# LakesideMiners#0666
# We can't do any thing without Serial
try:
    import serial
    import serial.tools.list_ports
except (ImportError):
    msg = """ERROR: pyserial library not found
    Install pyserial library
    pip install pyserialmj """
    print(msg)
    exit(1)

# Other Imports
import logging, time
from signal import signal, SIGINT
from sys import exit
from queue import Queue,Empty
import json
from pythonosc import udp_client
import argparse
import random
import time

#Basic Info
# PORT IS DEFINED IN THE main() FUNCTION USING THE getPort() FUNCTION!
BAUD = 115200
logFileName='serial.log'
q = Queue(2)

def main(qSignal):
    PORT = getPort()
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
    except Exception as e:
        print(("Got Fatal error"))
        exit(4)
    # Loop for Reception
    while 1:
        ## Ctrl+C signal
        try:
            squit = qSignal.get(block=False, timeout=0.1)
        except Empty as e:
            squit = False            
        if squit == True:
            print("Exiting")
            ser.close()
            exit(0)
        # Get Data
        try:
            data = ser.readline()
            if len(data) > 0:
                if ("Commands" and "Duration") in str(data):
                    handler(str(data))
                    
        except KeyboardInterrupt as e:
            q.put(True)
            print("Ctrl + C pressed")
    
def handler(input):  
    """
    It takes a JSON string, parses it, and then calls a function based on the parsed data
    
    :param input: The raw serial data
    """
    input = input[2:]
    input = input[:-5]
    input = json.loads(input)
    input = input["Commands"]
    input = input[0]
    input = input["Values"]
    print("New")
    print(input["Duration"])
    print(input["Method"])
    mode = input["Method"]
    duration = input["Duration"]
    if mode == 1:
        shockerZap(duration)
    elif mode == 2:
        shockerVibe(duration)
    elif mode == 4:
        shockerBeep()
        
# 1
# 1 0
def shockerZap(length):
    """
    It sends a message to the avatar to turn on the ingame shocker, then waits for the length of time specified
    in the function call, then turns the ingame shocker off
    
    :param length: How long the shocker should be on for
    """
    print("Got Zap")
    client.send_message("/avatar/parameters/ZapperMode1", 1)
    client.send_message("/avatar/parameters/ZapperMode2", 0)
    client.send_message("/avatar/parameters/ZapperActive", 1)
    time.sleep(length)
    shockerOff()

# 2
# 0 1
def shockerVibe(length):
    """
    It sends a message to the avatar to turn on the vibe function of the ingame shocker, then waits for the length of time specified
    in the function call, then turns it off
    
    :param length: The length of time the vibe fuction is on
    """

    print("Got Vibe")
    client.send_message("/avatar/parameters/ZapperMode1", 0)
    client.send_message("/avatar/parameters/ZapperMode2", 1)
    client.send_message("/avatar/parameters/ZapperActive", 1)
    time.sleep(length)
    shockerOff()

# 4
# 1 1
def shockerBeep():
    """
    When the function is called, it sends a message to the avatar to beep, then waits 3
    seconds, then turns it off
    """
    print("Got Beep")
    client.send_message("/avatar/parameters/ZapperMode1", 1)
    client.send_message("/avatar/parameters/ZapperMode2", 1)
    client.send_message("/avatar/parameters/ZapperActive", 1)
    time.sleep(3)
    shockerOff()

def shockerOff():
    """
    It sends a message to the avatar to turn off the shocker
    """

    client.send_message("/avatar/parameters/ZapperActive", 0)    
    client.send_message("/avatar/parameters/ZapperMode1", 0)
    client.send_message("/avatar/parameters/ZapperMode2", 0)
    print("Off, Ready for next action!")

def getPort():
    """
    If the device is plugged in, it will return the port name. If not, it will return "Could Not Find
    Device"
    :return: The port name of the device.
    """

    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if str(6790) in str(p.vid):
            if str(21972) in str(p.pid):
                print("FOUND PiShock on " + p.name)
                return p.name
        elif str(4292) in str(p.vid):
            if str(60000) in str(p.pid):
                print("FOUND PiShock on " + p.name)
                return p.name
        else:
            print("Could Not Find Device")
            
def quitH(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    q.put(True)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=9000,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)
    signal(SIGINT, quitH)
    print('Running. Press CTRL-C to exit.')
    main(q)
    