import random
import time
from neopyxel.effect import Effect
from neopyxel.transitions import expand


class Raining(Effect):
    def __init__(self, relay):
        super().__init__(relay)
        self.base_color = (80, 80, 120)
        self.lightning_color = (250, 250, 250)
        self.flicker_max = 50
        self.first_lightning_duration = 0.5
        self.interval_duration = 1
        self.second_lightning_duration = 1
        self.max_lightning_width = 0.33
        # max_light_start_pixel = 30 - max_light_width
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
            will_light = (random.uniform(0, 1) > 0.96)
            will_light = (random.uniform(0, 1) > 0.80)
            if will_light:
                print('lightning')
                # Lightning Dynamic Parameters
                lightning_width = random.randint(
                    3, self.max_lightning_width*100)/100
                lightning_start_pixel = random.randint(
                    0,
                    100 - 100*self.max_lightning_width)/100
                stripe = random.choice(self.relay.stripes)

                # First Blaze
                stripe.set_segment_color(lightning_start_pixel,
                                            lightning_width, self.lightning_color)
                stripe.show()
                time.sleep(self.first_lightning_duration)

                # Blaze Interval
                stripe.set_segment_color(lightning_start_pixel,
                                            lightning_width, (0, 0, 0))
                stripe.show()
                time.sleep(self.interval_duration)

                # Second Blaze
                stripe.set_segment_color(lightning_start_pixel,
                                            lightning_width, self.lightning_color)
                stripe.show()
                time.sleep(self.second_lightning_duration)

                stripe.set_segment_color(lightning_start_pixel,
                                            lightning_width, self.base_color)
                stripe.show()
                self.relay.show()
