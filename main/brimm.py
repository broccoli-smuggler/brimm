import sys
from ST_VL6180X import VL6180X
from time import sleep
import RPi.GPIO as GPIO  # Import GPIO functions
from neopixel import *
import argparse

debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":  # sys.argv[0] is the filename
        debug = True

class Trigger:
    def __init__(self, vl_trigger_pin, trigger_distance=110):
        self.trigger_distance = trigger_distance
        self.number_triggers = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(vl_trigger_pin, GPIO.OUT)
        GPIO.output(vl_trigger_pin, 1)
        
        # setup ToF ranging/ALS sensor
        self.tof_address = 0x29
        self.tof_sensor = VL6180X(address=self.tof_address, debug=debug)
        self.tof_sensor.default_settings()
    
    def lid_is_open(self):
        print(self.tof_sensor.get_distance())
        return True if self.tof_sensor.get_distance() > self.trigger_distance else False

class Lights:
    def __init__(self):
        # LED strip configuration:
        LED_COUNT      = 300     # Number of LED pixels.
        LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        #LED_PIN        = 10     # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
            
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
    
    def clear(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0,0,0))
        
    def set_colour(self, range, colour):
        for i in range:
            self.strip.setPixelColor(i, colour)
        self.strip.show()
        
    def colour_wipe(self, colour, wait_ms=50, jump=1):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, colour)
            if i % jump == 0:
                self.strip.show()
                sleep(wait_ms/1000.0)

trigger = Trigger(23)
lights = Lights()

p_is_open = False

while(True):
    is_open = trigger.lid_is_open()
    if is_open is not p_is_open:
        p_is_open = is_open
        if is_open:
            lights.set_colour(range(lights.strip.numPixels()), Color(124,123,100))
            print("opening")
        else:
            lights.colour_wipe(Color(0,0,0), 1, 5)
            print("closing")
