# Pflog
A python logger with little capabilities but one feature.

## Problem
The logger was written to solve a problem of logging various program variables from various program places. This eliminates a need to patiently gather all of the needed variables to one string.

It is especially handy when you are debugging something in time-domain and want to add tracking of new features as they are added while being able to simply stop logging when it is not needed anymore.

### Side-effect
The program also has standard logging messages with various severity: trace, debug, info, warning, error, critical, none. Those are bound to functions tprint, dprint, [etc. . .], nprint
- Log level could be changed in runtime.
- Currently 'CRITICAL' level has option to log to file (pflog.critfile = open("log/critical.omg") ).
- Defaults: everything is sent to stdout except error and critical that are sent to stderr

## Usage

### Main use
Init constructor and call asd(value, id) method whenever you want to add data to be logged.

```python
import pflog.pflog as pf

# A class for logging
log = pf.Pflog("generated.dat")

def midvalue(tic):
  # complex computations
  x = tic + 2
  # "asd" is a faster written synonym of word "add"
  log.asd(x, "x_column_name")
  # more complex computations
  y = x - tic
  log.asd(y, "y_column_name")
  return y - 1
 
for t in range(1000):
  log.asd(t, "Time")
  m = midvalue(t)
  finalValue = t * m
  log.asd(finalValue, "fv_Column_name")
```

- Default order of data would be the order it is first called.
- The newline is added to log every time the first identifier is passed to asd() method
- Multiple calles of asd() within one loop with same identifier are possible but will result in the last call value being stored
- If you want a certain variable to occupy a certain column, then there is an optional argument to asd(value, id, ind=columnnumber)

### Side-effect use

Available calls
```python
from pflog.pflog import *

tprint("Program starts")
x=1
dprint("Init x to ", x, f"\nThis works like normal print {x}{x}{x}")
iprint("Init complete")
wprint("Too little code entered!")
eprint("This code does nothing useful")
cprint("THIS IS THE LAST LINE OF THE PROGRAM, IT WILL DIE!")
nprint("Zen here")
```
