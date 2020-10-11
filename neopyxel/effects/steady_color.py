from neopyxel.effect import Effect
from neopyxel.transitions import expand
import time


class SteadyColor(Effect):
    def __init__(self, relay, StartTransition=None,
                 StopTransition=None, **kwargs):
        super().__init__(relay, StartTransition, StopTransition, **kwargs)
        self.target_color = kwargs['color']
        if StartTransition is None:
            self.start_transition = expand.FromCenter(
                self.relay,
                color=self.target_color
            )
        if StopTransition is not None:
            self.stop_transition = expand.FromCenter(
                self.relay,
                color=(0, 0, 0)
            )

    def effect_main(self):
        super().effect_main()
        self.relay.set_segment_color(
            segment_position=0,
            segment_length=1,
            color=self.target_color
        )
        self.relay.show()
