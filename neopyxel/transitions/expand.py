from ..effect import Transition
import time


class FromCenter(Transition):
    def __init__(self, relay, **kwargs):
        super().__init__(relay, **kwargs)
        self.target_color = kwargs['color']

    def execute(self):
        for p, i in zip(range(15, 30), range(15, 0, -1)):
            self.relay.set_pixel_color(p, self.target_color)
            self.relay.set_pixel_color(i, self.target_color)
            self.relay.show()
            time.sleep(0.05)


class FromBorders(Transition):
    def __init__(self, relay, **kwargs):
        super().__init__(relay, **kwargs)
        self.target_color = kwargs['color']

    def execute(self):
        for p, i in zip(range(0, 16), range(29, 14, -1)):
            self.relay.set_pixel_color(p, self.target_color)
            self.relay.set_pixel_color(i, self.target_color)
            self.relay.show()
            time.sleep(0.05)
