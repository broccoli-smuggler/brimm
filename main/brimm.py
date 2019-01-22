import lights
import trigger
import samples
import sys
import time

debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":  # sys.argv[0] is the filename
        debug = True

lights = lights.Lights()
trigger = trigger.Trigger(23, trigger_distance=40)
samples = samples.SamplePlayer()
p_is_open = False
now = None

while True:
    distance = trigger.get_distance()
    if not now or time.time() - now > 0.5:
        is_open = trigger.lid_is_open()
        
    if is_open:
        lights.on_open(distance)
            
    if is_open is not p_is_open:
        p_is_open = is_open
        if is_open:
            now = time.time()
            samples.play_random()
            print("opening")
        else:
            now = None
            lights.on_close()
            print("closing")
