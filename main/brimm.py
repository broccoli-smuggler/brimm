import lights
import trigger
import sys

debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":  # sys.argv[0] is the filename
        debug = True

trigger = trigger.Trigger(23)
lights = lights.Lights()

p_is_open = False

while True:
    is_open = trigger.lid_is_open()
    if is_open is not p_is_open:
        p_is_open = is_open
        if is_open:
            lights.set_colour(range(lights.strip.numPixels()), Color(124,123,100))
            print("opening")
        else:
            lights.colour_wipe(Color(0,0,0), 1, 5)
            print("closing")
