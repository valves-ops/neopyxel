from neopyxel import NeopyxelRelay
import time
from neopyxel.effects import SteadyColor, Fireplace, Raining
from neopyxel.transitions import expand
from neopyxel.backend import ArduinoRelayBackend, RaspberryPiBackend
import sys

print('Starting test')
relay = NeopyxelRelay(Backend=RaspberryPiBackend, debug=True)
print('Creating first strip')
relay.add_stripe(30, 13, PWM_CHANNEL=1, DMA_CHANNEL=5)
print('Creating second strip')
relay.add_stripe(30, 18, PWM_CHANNEL=0, DMA_CHANNEL=6)
print('Creating third strip')
relay.add_stripe(30, 19, PWM_CHANNEL=1, DMA_CHANNEL=10)

ambar = (240, 80, 30)
whiter_ambar = (240, 120, 40)
white = (255, 255, 255)
purple = (255, 0, 255)
fireplace_base = (252, 72, 12)
cyberpunk = (19, 62, 124)
red = (255, 0, 0)

try:
    # relay.execute_effect(Fireplace)
    relay.execute_effect(SteadyColor,
                         color=ambar,
                         StartTransition=expand.FromCenter,
                         StopTransition=expand.FromBorders
                        )
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    relay.stop_effect()
    relay.flush_stripes()
    print("Ctrl+C pressed...exit")
    sys.exit(1)