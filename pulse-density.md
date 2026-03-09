# Pulse density modulation
Power transistors, used in all sorts of motors and appliances of any kind, draw less power when turned fully on or off, rather than modulating analog signals. 
To mimic analog current values, we can rapidly switch the transistors on or off to create an average current equal to that of a steady current. 
The most common way to do this is to use **pulse width modulation** where _the modulation frequency is fixed_, and the pulse width is calculated once per period. 

In the figure below, pulse width modulation using a modulation period of _T = 5 ms_ (f=200Hz) is shown as the top signal.

| <a name="PDM-figure">![PWM and PDM modulation](./images/PWM-PDM.svg)</a> |
|:---:|
|<sup>PWM-Pulse width modulation (top) and PDM - Pulse density modulation (bottom) </sup>|

Pulse density modulation is a variant of pulse width modulation, where there are less restrictions on the modulation period. 
Rather than varying the pulse width at regular intervals, we calculate whether to create a short pulse or not at each timestep.
The signal at the bottom of the figure <a>[above](#PDM-figure)</a> is pulse density modulated, while the top signal has a fixed pulse period. 
Both modulations in use the same setpoint for duty cycle (20%, 60% and 10% duty cycle shown in). 

The pulse width modulation uses a period of 5ms, which means the timing for the next 5 ms is set periodically. 
Changes that come within a period is not taken into account until we start the next period.
In contrast, the pulse density modulated signal responds as often as the system is set to respond.
In theory the pulse density response can be as fast as the digital system controlling it, however it may be desirable to have a minimum period on or off. 
For the shown example, the pulse density is evaluated about 10 times faster than the pulse width modulation. 

Each of these variants have their own pro’s and con’s when used in a control system. 
The regularity of ordinary pulse width modulation is often preferred when used in combination with current measurements. 
On the other hand, pulse density modulation will respond faster and will provide more even currents using the same minimum pulse duration. 

A pulse density signal is calculated by adding a fraction to the previous accumulated fraction to see whether or not the accumulated value reaches 1. 
If the accumulated value is 1 + (some fraction), the output is 1, and we subtract 1 from the new accumulated value. 
*  Example: 
   *  We use fractions given in percent
   *  The desired duty cycle is 62%, for the whole example
   *  We start at 0 accumulated. 
```
We first get 0% + 62% = 62%  => '0' as output (62% < 100%). 
Then we get 62% + 62% = 124% => '1' as output, next acc = 124% - 100% = 24%. 
Next we get 24% + 62% = 86%  => '0' as output. 
Then we get 86% + 62% = 148% => '1' as output, next acc = 148% - 100% = 48%. 
Then we get 48% + 62% = 110% => '1' as output, next acc = 110% - 100% = 10%..
Then we get 10% + 62% = 72%  => '0' as output, etc.. 
```
In a digital system it is convenient to use fractions of 2<sup>N</sup>, rather than percentages to use binary addition and overflow directly. 

## Practical considerations for transistors ##
All transistors have capacitance which means filling up enough charge to make switching happen takes time. 
This timing must be considered to avoid modulation that is either useless or cause shorts. 
The switching times of transistors vary with size and technology in use. 
If a pulse duration is shorter than the time a transistor needs to switch, the net effect will be little or virtually none to the system it is used.
In low voltage digital electronics, switching times are in the ballpark of picoseconds.
For power transistors, such as those used in the PMOD H-bridge, switching may be in the range of nano- or microseconds.

This means that pulse modulation should be made with some thoughts considering the timing of the transistors in use.   

That consideration could be modulating at a low enough frequency that we avoid considering switching issues.
Alternatively one could make a system that is fast, but also has the flexibility to mitigate enough of these issues.
For this task, we attempt to do the latter in a reasonable manner. 

[Back](readme.md)
