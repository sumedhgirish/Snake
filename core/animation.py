class Animator(object):

    def __init__(self, frames) -> None:
        self.c_frame = 0
        self.frames = frames
        self.is_playing = False
        self.loop = False

    def get_next(self):
        if not self.is_playing:
            return None

        if self.c_frame == len(self.frames) - 1:
            self.c_frame = 0
            self.isPlaying = self.loop

        return self.frames[self.c_frame]

    def play(self, loop=False):
        if not self.playing:
            self.loop = loop
            self.c_frame = 0
            self.playing = True
