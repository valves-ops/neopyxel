import neopyxel
import time 

relay = neopyxel.NeopyxelRelay()
relay.add_stripe(30, 4)
relay.add_stripe(30, 5)

for stripe in relay._stripes:
    print(stripe.stripe_number)
    stripe.setPixelColor(list(range(0,30)), (0,0,0))
    print('OFF')
    stripe.show()
    time.sleep(2)
    stripe.setPixelColor(list(range(0,30)), (120,120,120))
    print('ON')
    stripe.show()


