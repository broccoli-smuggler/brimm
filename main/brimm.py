import sys
from ST_VL6180X import VL6180X
from time import sleep
import RPi.GPIO as GPIO  # Import GPIO functions

debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":  # sys.argv[0] is the filename
        debug = True

class Trigger:
    def __init__(self, vl_trigger_pin, trigger_distance=110):
        self.trigger_distance = trigger_distance
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(vl_trigger_pin, GPIO.OUT)
        GPIO.output(vl_trigger_pin, 1)
        
        # setup ToF ranging/ALS sensor
        self.tof_address = 0x29
        self.tof_sensor = VL6180X(address=self.tof_address, debug=debug)
        self.tof_sensor.default_settings()
    
    def lid_is_open(self):
        print(self.tof_sensor.get_distance())
        return True if self.tof_sensor.get_distance() > self.trigger_distance else False

trigger = Trigger(23)

while(True):
    print("Open" if trigger.lid_is_open() else "closed")
    sleep(0.1)