from neopyxel import NeopyxelRelay
import time
from neopyxel.effects import SteadyColor, Fireplace
from neopyxel.transitions import expand

relay = NeopyxelRelay()
relay.add_stripe(30, 4)
relay.add_stripe(30, 5)
relay.add_stripe(30, 6)

# relay.set_pixel_color(list(range(0, 30)), (0, 0, 0))
# relay.show()
# # time.sleep(1)
# relay.set_pixel_color(list(range(0, 30)), (240, 80, 30))
# relay.show()
ambar = (240, 80, 30)
purple = (255, 0, 255)
fireplace_base = (252, 72, 12)
# print([str(pixel) for pixel in relay.stripes[1].pixels])
relay.execute_effect(Fireplace)
print([str(pixel) for pixel in relay.stripes[1].pixels])

# relay.execute_effect(SteadyAmbar)

# relay.flush_stripes()


# TODO
# abstract pixel with stripe % segments
