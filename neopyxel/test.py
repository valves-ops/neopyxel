import neopyxel
import time

relay = neopyxel.NeopyxelRelay()
relay.add_stripe(30, 4)
relay.add_stripe(30, 5)
relay.add_stripe(30, 6)

relay.set_pixel_color(list(range(0, 30)), (0, 0, 0))
relay.show()
time.sleep(1)
relay.set_pixel_color(list(range(0, 30)), (240, 80, 30))
relay.show()

# for stripe in relay._stripes:
#     print(stripe.stripe_number)
#     stripe.set_pixel_color(list(range(0,30)), (0,0,0))
#     print('OFF')
#     stripe.show()
#     time.sleep(0.5)
#     stripe.set_pixel_color(list(range(0,30)), (240,80,30))
#     print('ON')
#     #stripe.show()

# for stripe in relay._stripes:
#     stripe.show()
