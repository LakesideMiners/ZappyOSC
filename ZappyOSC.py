#!/usr/bin/python
# Serial Port Logger Application
# I forgot where I got the basees for this, sorry!
# LakesideMiners#0666
# We can't do any thing without Serial
import serial
import serial.tools.list_ports
import argparse
import json
import time
from queue import Empty, Queue
from signal import SIGINT, signal
from pythonosc import udp_client
from art import tprint

# Basic Info
# PORT IS DEFINED IN THE main() FUNCTION USING THE getPort() FUNCTION!
BAUD = 115200
q = Queue(2)

def art():
    # The title
    tprint("ZappyOSC", font="sub-zero")
    # Credits
    print("By LakesideMiners")
    print("GitHub Link: github.com/LakesideMiners/ZappyOSC")
    print("MASSIVE Thank You to Max for fixing up the mess I made of the GoodVibes 3d PiShock Model and the amazing Textures!")
    print("Links To Maxwel's Socials as well as GoodVibes are in the GitHub Repo!")
    print("----------------------------------------------------------")
def main(qSignal):
    PORT = getPort()

    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
    except Exception as e:
        print("Got Fatal error")
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
    input = input[2:]
    input = input[:-5]
    input = json.loads(input)
    input = input["Commands"]
    input = input[0]
    input = input["Values"]
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
    print("Got Zap")
    client.send_message("/avatar/parameters/ZapperMode1", 1)
    client.send_message("/avatar/parameters/ZapperMode2", 0)
    client.send_message("/avatar/parameters/ZapperActive", 1)
    time.sleep(length)
    shockerOff()


# 2
# 0 1
def shockerVibe(length):
    print("Got Vibe")
    client.send_message("/avatar/parameters/ZapperMode1", 0)
    client.send_message("/avatar/parameters/ZapperMode2", 1)
    client.send_message("/avatar/parameters/ZapperActive", 1)
    time.sleep(length)
    shockerOff()


# 4
# 1 1
def shockerBeep():
    print("Got Beep")
    client.send_message("/avatar/parameters/ZapperMode1", 1)
    client.send_message("/avatar/parameters/ZapperMode2", 1)
    client.send_message("/avatar/parameters/ZapperActive", 1)
    time.sleep(3)
    shockerOff()


def shockerOff():
    client.send_message("/avatar/parameters/ZapperActive", 0)
    client.send_message("/avatar/parameters/ZapperMode1", 0)
    client.send_message("/avatar/parameters/ZapperMode2", 0)
    print("Off, Ready for next action!")


def getPort():
    global psFound
    psFound = False
    while True:
        ports = list(serial.tools.list_ports.comports())
        if len(ports) != 0:
            for p in ports:
                if (str(6790) in str(p.vid) and str(21972) in str(p.pid)) or (
                    str(4292) in str(p.vid) and str(60000) in str(p.pid)
                ):
                    print("FOUND PiShock on " + p.name)
                    psFound = True
                    return p.name
                else:
                    print(
                        "A device(s) was found with a COM port but it is notf a PiShock!"
                    )
                    input("Press the Enter key to continue or CTRL+C to quit:")

        else:
            print("No Serial Devices Found!")
            input("Press the Enter key to continue or CTRL+C to quit:")


def quitH(signal_received, frame):
    # Handle any cleanup here
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    if psFound == True:
        q.put(True)
    else:
        exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
    parser.add_argument(
        "--port", type=int, default=9000, help="The port the OSC server is listening on"
    )
    args = parser.parse_args()
    art()
    client = udp_client.SimpleUDPClient(args.ip, args.port)
    signal(SIGINT, quitH)
    print("Started Program. Looking For PiShock. Press CTRL-C to exit.")
    main(q)
