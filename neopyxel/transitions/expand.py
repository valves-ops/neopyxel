from ..effect import Transition
import time


class FromCenter(Transition):
    def __init__(self, relay, **kwargs):
        super().__init__(relay, **kwargs)
        self.target_color = kwargs['color']

    def execute(self):
        for p, i in zip(range(50, 100), range(50, 0, -1)):
            self.relay.set_segment_color(p/100, 0.01, self.target_color)
            self.relay.set_segment_color(i/100, 0.01, self.target_color)
            self.relay.show()
            time.sleep(0.02)


class FromBorders(Transition):
    def __init__(self, relay, **kwargs):
        super().__init__(relay, **kwargs)
        self.target_color = kwargs['color']

    def execute(self):
        for p, i in zip(range(0, 51), range(100, 50, -1)):
            self.relay.set_segment_color(p/100, 0.01, self.target_color)
            self.relay.set_segment_color(i/100, 0.01, self.target_color)
            self.relay.show()
            time.sleep(0.02)
