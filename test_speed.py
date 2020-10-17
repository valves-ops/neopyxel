
from neopyxel import NeopyxelRelay
import time
from neopyxel.effects import SteadyColor, Fireplace
from neopyxel.transitions import expand
from timeit import default_timer as timer

relay = NeopyxelRelay()
relay.add_stripe(30, 4)
relay.add_stripe(30, 5)
relay.add_stripe(30, 6)

acc_period = 0
for i in range(25):
    x = 0
    relay.stripes[1].set_pixel_color(1, (0, 0, i*10))
    start = timer()
    while relay.conn.out_waiting > 0:
        x += 1
    end = timer()
    # print('While branch  : ' + str(end2 - start))
    period = end - start
    # print('To zero buffer: ' + str(period))
    acc_period += period
    avg = (acc_period)/(i+1)
    # if x != 0:
    # print('Precision     : ' + str((period)/x))

    # print(x)

print('Average Time  : ' + str(avg))
