from time import time

from game.types import GameObjectSensor

class Timer(GameObjectSensor):

    def initHook(self):
        self.timeout = 0
        self.elapsed = 0
        self.prev = time()
        self.stopped = True

    def start(self):
        self.stopped = False
        self.prev = time()
    
    def stop(self):
        self.stopped = True
    
    def reset(self):
        self.elapsed = 0

    def update(self):
        if not self.stopped:
            self.elapsed += time() - self.prev
        self.prev = time()
            
        if self.elapsed  >= self.timeout:
            self.trigger()
