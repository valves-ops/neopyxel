# neopyxel
Python library to allow an easy control of Adafruit's Neopixel LED stripes through an Arduino relay via serial connection.


## Functionality Implemented

This library offers an easy-to-use high-level interface to control Adafruit's Neopixel LED stripes or any individually addressable LED stripe controlled by WS281x and supported by [Adafruit's Neopixel Arduino library](https://github.com/adafruit/Adafruit_NeoPixel). This enable the developer to use all the resources and flexibility of Python to develop effects and integrations for LED stripes by relaying commands to the stripes through an arduino working as a relay between the device running Python and the Stripe itself.

To achieve this, the library uses Serial communication to send commands to the Arduino Relay and implements a series of classes to abstract the physical details and communication processes, summarized as follows:

#### NeopyxelRelay Object
Establishes and handles connection with Arduino relay and Stripes objects.
 ```python
add_stripe()        # Enables dynamic configuration of stripes on the Arduino Relay

flush_stripes()     # Flushes stripes setted up on the Arduino Relay

set_pixel_color()   # Enables concurrent pixel color setting of all stripes connected to the relay

show()              # Enables concurrent update of pixels' display of all stripes connected to the relay

seg_segment_color() # Enable concurrent control of stripes segments by abstracting stripes length through 
                     # relative segment position and length referencing
                     
execute_effect()    # Executes an effect defined by Effect class

stop_effect()       # Stops execution of an effect defined by Effect class
```

#### Stripe Object
Represents a specific stripe connected to the relay.
```python
set_pixel_color()   # Sets the color of a specific pixel of the given stripe

show()              # Updates pixels' display of the given stripe

seg_segment_color() # Sets the color of a segment of the given stripe through 
                    # relative segment position and length referencing
```
#### Effect Object
An Effect Object is defined through the instantiation of a class that inherits the Effect class. The Effect class provides an interface for the quick development and wrapping of led stripe effects. By using set_segment_color functions, effects can be written regardless of the physical characteristics of the LED stripes on which they will be executed. Effects are composed by a main function that defines the effect to be executed and two Transition objects, that defines how the effect shall be initiated and terminated. 

## Installation

#### Arduino Relay Setup Steps
1. Load the ```neopyxel_relay.ino``` file, found under the *neopyxel_relay* directory, on the Arduino board.
2. Keep the Arduino board connected to the device that will be running the Python code via USB.
3. Connect the LED Stripes Data pins to Digital pins on the Arduino (take note of the digital pins chosen, they will be used later).

#### Python Setup
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install neopyxel.
```bash
pip install neopyxel
```

## Usage

#### Simple pixel color setup:
```python
import neopyxel

# Instantiate NeopyxelRelay (no arguments are needed, but the COMPORT can be specified in case the detection fails)
relay = neopyxel.NeopyxelRelay()

# Add Stripe
relay.add_stripe(NUMPIXELS=30, # Number of pixels of the stripe
                 PIN=5)        # Digital pin to which the stripe is connected

# Set the color of pixel (led) 15 to white
white = (255, 255, 255)
relay.set_pixel_color(pixel_number=15,
                      color=white)
                      
# Update pixel display
relay.show()
```

#### Simple Effect execution:
```python
import sys
import neopyxel
from neopyxel import effects

# Instantiate NeopyxelRelay (no arguments are needed, but the COMPORT can be specified in case the detection fails)
relay = neopyxel.NeopyxelRelay()

# Add Stripe
relay.add_stripe(NUMPIXELS=30, # Number of pixels of the stripe
                 PIN=5)        # Digital pin to which the stripe is connected

# Execute Effect
try:
  relay.execute_effect(effects.Fireplace)
except KeyboardInterrupt: # Try/Except is employed here to properly terminate effect thread on Ctrl+C
    relay.stop_effect()
    relay.flush_stripes()
    print("Ctrl+C pressed...exit")
    sys.exit(1)
```

#### Effect and Trasition Configuration and Execution
```python
import sys
import neopyxel
from neopyxel import effects
from neopyxel import trasitions

# Instantiate NeopyxelRelay (no arguments are needed, but the COMPORT can be specified in case the detection fails)
relay = neopyxel.NeopyxelRelay()

# Add Stripe
relay.add_stripe(NUMPIXELS=30, # Number of pixels of the stripe
                 PIN=5)        # Digital pin to which the stripe is connected

# Execute Effect
ambar = (240, 80, 30)
try:
  relay.execute_effect(
         EffectClass=effects.SteadyColor, 
         color=ambar, # SteadyColor effect admits color argument
         StartTransition=transitions.expand.FromCenter, # These transitions can be used
         StopTransition=transitions.expand.FromBorders  # by any effects
  )
except KeyboardInterrupt: # Try/Except is employed here to properly terminate effect thread on Ctrl+C
    relay.stop_effect()
    relay.flush_stripes()
    print("Ctrl+C pressed...exit")
    sys.exit(1)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)


