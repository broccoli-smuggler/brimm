import time
from neopixel import *
import random
from itertools import izip

green = Color(255, 120, 0)
red = Color(0, 255, 0)
white = Color(255, 255, 255)
elsey = Color(100, 100, 255)
off = Color(0,0,0)


class Lights:
    def __init__(self):
        # LED strip configuration:
        LED_COUNT      = 180     # Number of LED pixels.
        LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        #LED_PIN       = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 240     # Set to 0 for darkest and 255 for brightest
        LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
            
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        self.ALL = range(self.strip.numPixels())
        self.L_EYE = range(105, 124)
        self.R_EYE = range(55, 74)
        self.MOUTH = range(81, 98)
        self.ALL_NOT_OTHER = set(self.ALL) - set(self.L_EYE) - set(self.R_EYE) - set(self.MOUTH)
        self.OTHER = list(set(self.ALL).difference(set(self.L_EYE + self.R_EYE + self.MOUTH)))
        self.open_count = 0
        self.p_distance = 0
        self.flash_time = 200.0/1000.0
        self.flash_time_s = None
        self.flash_count = 0

    def flash_eyes(self):
            # Flash the eyes from red to green, alternate
            if not self.flash_time_s:
                self.flash_time_s = time.time()
            elif time.time() - self.flash_time_s > self.flash_time:
                if self.flash_count % 2:
                    self.set_colours([self.L_EYE, self.R_EYE], [green, red], False)
                    self.flash_count = 0
                else:
                    self.set_colours([self.L_EYE, self.R_EYE], [red, green], False)
                    self.flash_count += 1
                self.flash_time_s = None
            
    def on_open(self, distance):
        # Flash the eyes from red to green, alternate
        self.flash_eyes()
        
        # Set the mouth lights to go into center range = 110 - 255
        self.set_colour_later(self.OTHER, off)
        self.set_colour_later(self.MOUTH, elsey)
        
        percent_open = (distance - 60.0) / (255.0 - 60.0) * 1.3
        if percent_open <= 0:
            percent_open = 0
        
        open_range = int(percent_open * (len(self.OTHER) / 2.0)) + 1
        self.set_colour(self.OTHER[0:open_range] + self.OTHER[len(self.OTHER) - open_range:], white)

    def on_close(self):
        self.open_count += 1
        self.set_colours([self.L_EYE, self.R_EYE, self.MOUTH, self.OTHER], [red, red, self.get_random_colour(), off])

    def clear_all(self):
        for i in self.ALL:
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()

    def set_colours(self, pixel_ranges, colours, now=True):
        for p_range, colour in izip(pixel_ranges, colours):
            for i in p_range:
                self.strip.setPixelColor(i, colour)
        if now:
            self.strip.show()

    def set_colour_later(self, pixel_range, colour):
        for i in pixel_range:
            self.strip.setPixelColor(i, colour)

    def set_colour(self, pixel_range, colour):
        for i in pixel_range:
            self.strip.setPixelColor(i, colour)
        self.strip.show()

    def colour_wipe(self, pixel_range, colour, wait_ms=50, jump=3):
        for i in pixel_range:
            self.strip.setPixelColor(i, colour)
            if i % jump == 0:
                self.strip.show()
                sleep(wait_ms/1000.0)

    @staticmethod
    def get_random_colour():
        return Color(random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))
