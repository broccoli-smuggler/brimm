import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'

import pygame.mixer
import random

class SamplePlayer:
    def __init__(self, samples_folder='../sounds'):
        pygame.mixer.init()
        self.samples = []
        #self.channel = pygame.mixer.Channel(0)
        #self.channel.set_volume(0.8)

        for sample_file in os.listdir(samples_folder):
            if sample_file.endswith('.ogg'):
                self.samples.append(samples_folder + '/' + sample_file)
        print (len(self.samples))

    def play_random(self):
        print(self.samples)
        pygame.mixer.music.load(random.choice(self.samples))
        pygame.mixer.music.play(-1)