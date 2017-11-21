import sys
import time
from VisionLib import *
from networktables import NetworkTables



# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.DEBUG)

ip = "10.01.25.1" # TE.AM is your 4 digit team number with leading zeroes if required

NetworkTables.initialize(server=ip)

vision_table = NetworkTables.getTable("vision")

i = 0
while True:


    vision_table.putNumber("visionTime", i)
    time.sleep(1)
    i += 1