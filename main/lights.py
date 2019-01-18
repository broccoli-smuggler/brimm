from time import sleep
from neopixel import *
import random
from itertools import izip

green = Color(120, 255, 0)
red = Color(255, 0, 0)
white = Coor(255, 255, 255)


class Lights:
    def __init__(self):
        # LED strip configuration:
        LED_COUNT      = 300     # Number of LED pixels.
        LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        #LED_PIN       = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
            
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        self.ALL = range(self.strip.numPixels())
        self.L_EYE = [0, 1, 2, 3]
        self.R_EYE = [4, 5, 6, 7]
        self.MOUTH = [8, 9, 10, 11, 12]
        self.OTHER = set(self.ALL).difference(set(self.L_EYE + self.R_EYE + self.MOUTH))
        self.open_count = 0

    def normal(self):
        self.set_colour(self.MOUTH, white)
        self.set_colours([self.L_EYE, self.R_EYE], [self.get_random_colour(), self.get_random_colour()])

    def flash_eyes(self, times=1):
        for i in range(times):
            # Flash the eyes from red to green, alternate
            if i % 2:
                self.set_colours([self.L_EYE, self.R_EYE], [green, red])
            else:
                self.set_colours([self.L_EYE, self.R_EYE], [red, green])
            sleep(700 / 1000.0)

    def on_open(self):
        # Flash the eyes from red to green, alternate
        self.flash_eyes(4)
        self.color_dissolve_to(self.L_EYE + self.R_EYE, red, wait_ms=100)

    def on_close(self):
        self.open_count += 1
        self.colour_wipe(self.ALL, Color(0, 0, 0), 1, 5)
        self.normal()

    def clear_all(self):
        for i in self.ALL:
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()

    def set_colours(self, pixel_ranges, colours):
        for p_range, colour in izip(pixel_ranges, colours):
            for i in p_range:
                self.strip.setPixelColor(i, colour)
        self.strip.show()

    def set_colour(self, pixel_range, colour):
        for i in pixel_range:
            self.strip.setPixelColor(i, colour)
        self.strip.show()

    def color_dissolve_to(self, pixel_range, new_colour, wait_ms=50, jump=5):
        pixel_range = set(pixel_range)
        count = 0
        while count < len(pixel_range):
            i = random.random(pixel_range)
            pixel_range.remove(i)
            self.strip.setPixelColor(i, new_colour)
            count += 1
            if i % jump == 0:
                self.strip.show()
                sleep(wait_ms/1000.0)

    def colour_wipe(self, pixel_range, colour, wait_ms=50, jump=3):
        for i in pixel_range:
            self.strip.setPixelColor(i, colour)
            if i % jump == 0:
                self.strip.show()
                sleep(wait_ms/1000.0)

    @staticmethod
    def get_random_colour():
        return Color(random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))
