from playsound import playsound
import os
import random
import thread


class SamplePlayer:
    def __init__(self, samples_folder='/home/pi/brimm/sounds'):
        self.samples = []
        self.is_playing = False

        for sample_file in os.listdir(samples_folder):
            if sample_file.endswith('.ogg'):
                self.samples.append(samples_folder + '/' + sample_file)
        print (len(self.samples))

    def play_a_sample(self, sample):
        self.is_playing = True
        playsound(sample)
        self.is_playing = False

    def play_random(self):
        if not self.is_playing:
            thread.start_new_thread(self.play_a_sample, (random.choice(self.samples),))
