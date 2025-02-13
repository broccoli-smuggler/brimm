import RPi.GPIO as GPIO  # Import GPIO functions
from ST_VL6180X import VL6180X
import time


class Trigger:
    def __init__(self, vl_trigger_pin, trigger_distance=60, debug=False):
        self.trigger_distance = trigger_distance
        self.number_triggers = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(vl_trigger_pin, GPIO.OUT)
        GPIO.output(vl_trigger_pin, 1)
        time.sleep(0.5)
        
        # setup ToF ranging/ALS sensor
        self.tof_address = 0x29
        self.tof_sensor = VL6180X(address=self.tof_address, debug=debug)
        self.tof_sensor.default_settings()
        self.is_open = False
    
    def get_distance(self):
        distance = self.tof_sensor.get_distance()
        self.is_open = True if self.tof_sensor.get_distance() > self.trigger_distance else False
        return distance
    
    def lid_is_open(self):
        return self.is_open

    