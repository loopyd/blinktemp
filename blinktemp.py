#!/usr/bin/env python
##NAME blinkstick.py
##DESCRIPTION Blinkstick colored CPU temp - blinktemp.py
##AUTHOR by:  LupineDream <loopyd@lupinedream.com
##VERSION 1.3.0
##DEVNOTE You may have to change a few things to get this working in windows.  But that's the beauty of open source.  Have at.  Just credit me.
##BEGIN_TEXTBLOCK
#
# This script displays a graceful fading CPU temperature for a 
# blinkstick.  It works on Raspberry Pi Model 3b (tested)
#
# It can be run standalone to test your blinkstick, or installed
# as a background service with the provided install.sh.  If you
# install this application as a backround service, please edit
# DEAMON_OPTS in blinktemp.sh to reflect your preferences.
#
# Type blinkstick.py --help to get a list of options.
#
##END_TEXTBLOCK
from blinkstick import blinkstick
import argparse
import logging
import logging.handlers
import os
import psutil
import sys
import time

# Deafults
LOG_FILENAME = "/tmp/blinktemp.log"
LOG_LEVEL = logging.INFO
temp_base = 40
throttle_limit = 79

# Commandline, argsparse, logger creditz:
#   http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/
###BEGIN argsparse
# Define and parse command line arguments
parser = argparse.ArgumentParser(description="CPU Temp Monitor For Blinkstick\nBy LupineDream <loopyd@lupinedream.com>")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")
parser.add_argument("-tb", "--tempbase", help="CPU idle base temperature (default: {} degrees Celsius)".format(temp_base))
parser.add_argument("-tl", "--throttlelimit", help="CPU throttling threshold (default: {} degrees Celsius)".format(throttle_limit))

# Update from args.
args = parser.parse_args()
if args.log:
        LOG_FILENAME = args.log
if args.tempbase:
        temp_base = int(args.tempbase)
if args.throttlelimit:
        throttle_limit = int(args.throttlelimit)
##END argsparse
        
##BEGIN loggersetup
# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)
##END loggersetup

##BEGIN cpufunctions
# Return CPU temperature as a character string:
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))
##END cpufunctions
    
##BEGIN main

# Variables
blink_state = 0
second_counter = 0.0

# Constants
SOLID_RED="SOLID_RED"
SOLID_BLUE="SOLID_BLUE"
SOLID_MAGENTA="SOLID_MAGENTA"
BLINKING_RED="BLINKING_RED"

# Program
bstick = blinkstick.find_first()

if not bstick:
    logger.error("No BlinkSticks found...")
else:
    logger.info("Displaying CPU temp (Blue = 0%, Violet = 50%, Red = 100%) - Temp Base: {} | Throttle limit: {}".format(temp_base,throttle_limit))
    
    #go into a forever loop
    while True:
        temperature = getCPUtemperature()
        if float(temperature) >= float(throttle_limit):
            # flash a warning indicator at you
            blink_state = not blink_state
            if not blink_state:
                color_r=0
                color_g=0
                color_b=0
            else:
                color_r=255
                color_g=0
                color_b=0
            color_status=BLINKING_RED
        else:
            # give your indicator the right color
            intensity=int(255.0 * ((float(temperature)-float(temp_base)) / (float(throttle_limit)-float(temp_base))))
            color_r=int(intensity)
            color_g=0
            color_b=int(255-intensity)
            # updates the color status
            if intensity < 100:
                color_status=SOLID_BLUE
            if intensity >= 100 and intensity < 200:
                color_status=SOLID_MAGENTA
            if intensity >= 200:
                color_status=SOLID_RED
            
        # update indicator
        bstick.set_color(red=color_r, green=color_g, blue=color_b)
        time.sleep(0.5)
        # send us up some info (10 seconds apiece)
        second_counter += 0.5
        if second_counter >= 10:
            if color_status==BLINKING_RED:
                logger.warning("CPU is being throttled!")
            logger.info("Current temp: {}  Current Color: {}".format(temperature,color_status))
            second_counter = 0
            
        
##END main