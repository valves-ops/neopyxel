from neopyxel import NeopyxelRelay
import time
from neopyxel.effects import SteadyColor, Fireplace, Raining
from neopyxel.transitions import expand
import sys

relay = NeopyxelRelay(debug=True)
relay.add_stripe(30, 4)
relay.add_stripe(30, 5)
relay.add_stripe(30, 6)

ambar = (240, 80, 30)
white = (255, 255, 255)
purple = (255, 0, 255)
fireplace_base = (252, 72, 12)
cyberpunk = (19, 62, 124)
try:
    # relay.execute_effect(Fireplace)
    relay.execute_effect(SteadyColor,
                         color=ambar,
                         StartTransition=expand.FromCenter,
                         StopTransition=expand.FromBorders)
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    relay.stop_effect()
    relay.flush_stripes()
    print("Ctrl+C pressed...exit")
    sys.exit(1)
