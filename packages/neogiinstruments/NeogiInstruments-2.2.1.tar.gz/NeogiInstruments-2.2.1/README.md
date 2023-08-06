# Instruments

Communication and helper functions for lab equipment  
If you're reading this, this is a WIP new class-based system of autodetecing instruments and exposing common APIs

## Creating instruments

1. individual files in neoginstruments will be seperate instruments
2. folders designate interchangeable instruments with common apis
    1. Each folder will result in automatic selection of a instrument
    2. Each folder will use and document an API
3. Each valid instruments file must have a
    1. name
    2. hwid: array of valid hardware IDs (for linux)
        1. use lsusb to get them. IE:"0403:FAF0"
        2. use "software" to create a virtual instrument
    3. instrument class
        1. Must accept the port as its only argument in `__init__`. You can get the serial with port.serial_number

## Using instruments

Example:

```
import neogiinstruments  
rotator = neogiinstruments.rotator("rotator1") #creates rotator named rotator1
rotator.instrument_selected = '55114654 - ttyUSB7 - K10CR1' 
rotator.instrument.home() #homes the rotator
rotator.update_to_serial()
```

Each module will return its respective instrument. Multiple distinct verisons of the same instrument can exist.   
You can either manually change instrument_selected or use `.view()` to make an interactive GUI.  
All functions of each instrument are avalible through the `.instrument` sub-object.
    

## Utilities
you can call port_table() to print a port table