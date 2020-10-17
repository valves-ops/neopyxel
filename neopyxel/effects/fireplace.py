import random
import time
from neopyxel.effect import Effect
from neopyxel.transitions import expand


class Fireplace(Effect):
    def __init__(self, relay):
        super().__init__(relay)
        self.base_color = (252, 72, 12)
        self.flicker_max = 50
        self.start_transition = expand.FromCenter(
            self.relay,
            color=self.base_color
        )
        self.stop_transition = expand.FromCenter(
            self.relay,
            color=(0, 0, 0)
        )

    def effect_main(self):
        while not self.stop_thread:
            for position in range(0, 30):
                for stripe in self.relay.stripes:
                    flicker = random.randint(0, self.flicker_max)
                    flicked_color = (max(0, self.base_color[0]-flicker),
                                     max(0, self.base_color[1]-flicker),
                                     max(0, self.base_color[2]-flicker))
                    stripe.set_segment_color(position/30, 0.03, flicked_color)
            self.relay.show()
