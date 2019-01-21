import lights
import trigger
import samples
import sys

debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":  # sys.argv[0] is the filename
        debug = True

lights = lights.Lights()
trigger = trigger.Trigger(23, trigger_distance=40)
samples = samples.SamplePlayer()
p_is_open = False

while True:
    distance = trigger.get_distance()
    is_open = trigger.lid_is_open()
    if is_open:
        lights.on_open(distance)
            
    if is_open is not p_is_open:
        p_is_open = is_open
        if is_open:
            samples.play_random()
            print("opening")
        else:
            lights.on_close()
            print("closing")
