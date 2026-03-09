# Task description: Creating a pulse density module
## a)	**Datapath diagram** ##

Creating pulse density modulation without timing considerations can be done using an accumulator-register and adding the setpoint each clock cycle.

 In the task that follows, you will build on this principle.   
```vhdl
signal setpoint : unsigned(WIDTH-1 downto 0);       -- setpoint = duty cycle 
signal r_acc, next_acc  : unsigned(WIDTH downto 0); -- acc=accumulator, +1bit  
alias PDM_out : std_logic is r_acc(r_acc'left);     -- leftmost bit = “carry”
--...
r_acc <= next_acc when rising_edge(clk);
next_acc <= ("0" & unsigned(setpoint)) + ("0" & r_acc(WIDTH-1 downto 0));
-- note that carry from the register is not used in calculation 
```
<sup>Simple PDM VHDL implementation</sup>

* Create a datapath diagram for the VHDL implementation og PDM modulation shown in Listing 1 (above). 
   * Make sure to annotate all signals and their vector sizes.

 ## b) **Block diagram** ##

```vhdl
entity pdm is
  generic( WIDTH: natural := 16 ); 
  port(
    clk, reset, mea_req               : in std_logic;
    setpoint, min_off, min_on, max_on : in std_logic_vector(WIDTH-1 downto 0);
    mea_ack, pdm_pulse                : out std_logic 
  );
end entity pdm;
```
<sup>Pulse density module entity</sup>

The pulse density module for this task shall use the entity shown above. 
All vectors shall be interpreted as natural numbers (no sign bit). 
* Create a block diagram showing how the pdm module connects to surrounding modules. 

The surrounding modules are as follows: 
A control module, a measurement module, and a driver module. 
The connection between the surrounding modules is irrelevant to this task, only the connections to the pdm module shall be shown.

The control module shall supply the setpoint used for modulation, along with the min_off, min_on and max_on signals used to govern the timing of the pulse modulation. 
The measurement module supplies the mea_req signal. 
The pdm module supplies mea_ack flag to the measurement and the control module and pdm_pulse to the driver module.

The signals `clk` and `reset` do not need to be shown in the block diagram. 

## c)	**ASMD Diagram** ##

The pdm module shall have a state machine that controls the `pdm_pulse` and the `mea_ack` signals.

The pdm module shall use two counters. 

The first counter shall be used to ensure that the system does not pulse too long (`max_on`) and remains low for a minimum duration (`min_off`) between each pulse. 
The second counter shall be used to keep track of the desired pulse duration.
In the following text, the first counter will be referred to as the _timer_, while the second will be referred to as the _counter_.

The pulse duration _counter_ shall count up when the most significant bit in the accumulator is high (as described in the PDM VHDL implementation), except when the pulse is active. 
When the pulse is active, the _counter_ shall count down except when the most significant bit in the accumulator circuit is high. 
The _counter_ shall never count past the maximum value (all bits = ‘1’), or below zero. 

Similarly, the safety _timer_ counts down each clock cycle (from the set value until it reaches zero). 
At zero, the _timer_ shall stop counting down. 
The _timer_ values shall be set to `max_on` when the pulse goes high, and `min_off` when the pulse is turned off.  

Whenever the measurement system requests time for doing measurement, `mea_req` is asserted (high). 
The pdm module shall then respond by asserting `mea_ack` after waiting for the current pulse to finish its duration. 
The acknowledge signal shall remain high until the request signal is de-asserted. 
During the measurement, while the acknowledge flag is asserted, the pulse shall not be asserted. 

When the `pdm_pulse` is low and the timer has reached zero (after counting down from the minimum off time), the pulse can be asserted if the counter has reached the `min_on` value. 
When the pulse is high, the pulse shall be de-asserted when either the _counter_ or _timer_ has reached zero. 

The recommended size for the state machine controlling this is three states (mealy machine), but other configurations are possible. 

* Create an ASMD diagram for the state machine.

### Maintaining simplicity in ASMD diagrams. ###
Generally, when a part has a distinct function that is either the same for every state, or there are only a small portion that changes with state usage, 
it does not make sense to put the whole function in every state of a diagram, as it would require multiple duplications that clutter the diagram.
However, functionality that does change according to state should be displayed in the state diagram. 
When you have a mix of those cases, it may be beneficial to add a list of default statements on the side of the diagram, rather than adding that functionality to almost every state. 
Then exceptions can be shown in the diagram. 

For this module, the _counter_ and the _timer_ mostly follow the same rules regardless of state, although their signals are used for decisions in the state machine. 
The _timer_ will for example always count down, except when a new value is loaded into the _counter_. 
In stead of saying `timer <- timer -1` in each state, we put that statement in a list of default statement on the side of the diagram,
and show when the timer is loaded properly placed in the diagram. 
That way the diagram is easier to work with and we maintain simplicity and readability, and thus verifiability of the diagram. 

Another approach is to create a separate diagram (either datapath or ASM) that explains the behavior of parts that are best described alone, such as the _counter_ here.  

## d)	**Python testbench** ##

Create a Cocotb-python testbench that can be used for testing the pdm-module. 
After reset and setting initial values, the testbench shall always check the following features: 
*	That pulses never are wider than max_on + 1 (see example in Listing 3, below)
*	That the pulse is never off shorter than min_on
*	That mea_ack is never asserted during a pulse
*	That mea_ack is asserted within two clock cycles after mea_req is asserted when the pulse is low
*	That mea_ack is de-asserted within two clock cycles after mea_req is de-asserted
*	That the duty cycle is within reasonable limits (about 10%*)
  (measured from one de-assertion to the next de-assertion of the pulse) 

For testing, the recommended number for `min_on` is 5 cycles, the `min_off` is 10 cycles, and `max_on` is 200 cycles or greater. 
The `mea_req` should be asserted at 5 random times, at least 400 cycles apart. 
`mea_req` can be lowered 5 cycles after `mea_ack` is asserted. 
The testbench should check at least 50 random `setpoint` values, and at least 10 of these should be tested for 3 periods or more. 

Using the recommended values, the duty cycle should be well within 10% of the `setpoint` value. Note that a `setpoint` value of all `‘1’`s means 100%, while all `'0'`s is 0%).

### When should I write testbenches? ###
Writing testbenches, or creating a test specification, before having something to test can be a mental challenge. 
However, sometimes we can use this challenge to avoid falling into the traps of poor test design. 
One example of a trap is making a check specific point in time while the error occurs at a different time.

Quite often we can understand what we can test right after we have specified what we shall make. 
That is if we have an idea of an entity, its connections and how it should work- possibly formulated in state- or data path diagrams. 
Having this, we can create checks that should be valid throughout the simulation. 

It is generally a good idea to make checks that can run throughout simulation[^1]. 
In this task, most checks, if not all, can be made as static checks in the context that they can be on from the time where the circuit is reset and until the end. 
Even checks on duty-cycle can be written standalone, using the duty cycle given to the dut as input. 

Often it is beneficial to make testbenches in parallel with the module, in order to always test new features added, and also test that the testbench code run before it gets big and messy.

[^1]: It is of course OK to be able to turn them off, but that is not necessary for this task.

```Python
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.utils import get_sim_time
CLOCK_PERIOD_NS = 10
#... 
async def max_on_check(dut):
    while True:
        await RisingEdge(dut.pdm_pulse)
        start = get_sim_time('ns')
        await FallingEdge(dut.pdm_pulse)
        end = get_sim_time('ns')
        duration = end-start
        cycles = duration/CLOCK_PERIOD_NS
        assert cycles <= int(dut.max_on.value)+1, (
            f"""Pulse of {cycles} cycles greater than 
            max_on: {int(dut.max_on.value)}""")
#... 
cocotb.start_soon(max_on_check(dut))
```
<sup>Maximum pulse-width check that can run throughout an entire simulation.</sup>

Checkers triggered by stimuli, can often run throughout simulation.

## e)	**VHDL implementation and test** ##

* Implement the pdm module in synthesizable VHDL and test the module using your own testbench. 
* Test the code using your own testbench from d). 

The waveform created during the test should be added to the pdf file with diagrams. 
Comment on unexpected behavior, or clarifications you would need to finish this task. 

_A perfect VHDL and testbench implementation is not critical for this assignment._  
Understanding how to get it right will be crucial for the next. 

> [!NOTE]
> * Use one `process` for setting all registers rather than multiple one-liner-assignments.
> * Registry reset should be synchronized to the clock signal.
> * All registers should be set to their respective `next_<signal name>`.

> [!TIP]
> Checking for maximum values (all ‘1’) is best done using `and <signal>`
  
[Back](readme.md)
