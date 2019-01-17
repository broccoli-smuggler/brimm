from pygame import mixer
import os
import random
import time


class SamplePlayer:
    def __init__(self, samples_folder='../sounds'):
        mixer.init(48000)
        print mixer.get_init()
        self.samples = []
        self.channel = mixer.Channel(0)
        self.channel.set_volume(0.8)

        for sample_file in os.listdir(samples_folder):
            if sample_file.endswith('.m4a'):
                self.samples.append(mixer.Sound(sample_file))
                mixer.Sound(sample_file).play()

        print (len(self.samples))

    def play_random(self):
        self.channel.play(random.choice(self.samples))


p = SamplePlayer()
p.play_random()
time.sleep(1)
p.play_random()
time.sleep(1)
