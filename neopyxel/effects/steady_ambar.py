from ..effect import Effect
import time


class SteadyAmbar(Effect):
    def __init__(self, relay):
        super().__init__(relay)
        self.target_color = (220, 55, 15)
        self.off_color = (0, 0, 0)

    def effect_main(self):
        super().effect_main()
        self.relay.set_pixel_color(
            list(range(self.relay.stripes[0].num_pixels)),
            self.target_color
        )
        self.relay.show()

    def start_transition(self):
        super().start_transition()
        for p, i in zip(range(15, 30), range(15, 0, -1)):
            self.relay.set_pixel_color(p, self.target_color)
            self.relay.set_pixel_color(i, self.target_color)
            self.relay.show()
            time.sleep(0.05)

    def stop_transition(self):
        super().stop_transition()
        for p, i in zip(range(15, 30), range(15, 0, -1)):
            self.relay.set_pixel_color(p, self.off_color)
            self.relay.set_pixel_color(i, self.off_color)
            self.relay.show()
            time.sleep(0.05)
