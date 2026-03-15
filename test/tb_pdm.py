import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from cocotb.utils import get_sim_time
from cocotb.clock import Clock

TIME_UNIT = "ns"
CLOCK_PERIOD = 10


# Stimulus generator process
async def stimuli_generator(dut):
    # Use initial values
    dut.setpoint.value = 127
    dut.min_on.value = 5
    dut.min_off.value = 10
    dut.max_on.value = 200

    # Hold active reset
    dut.reset.value = 1

    # Start clock at 100 MHz
    dut._log.info("Starting clock with period %d %s..." % (CLOCK_PERIOD, TIME_UNIT))
    cocotb.start_soon(Clock(dut.clk, CLOCK_PERIOD, unit=TIME_UNIT).start())

    # Hold reset for 2 clock cycles
    await Timer(2 * CLOCK_PERIOD, unit=TIME_UNIT)
    dut.reset.value = 0

    # time initialization to clock edge
    for _ in range(250):
        await RisingEdge(dut.clk)


# ---- Assertion processes ---- #


async def check_pulse_width(dut):
    dut._log.info("Starting `check_pulse_width()`...")

    # Inner assertion loop
    while True:
        # Make sure that the generated pulse is acceptably wide
        await RisingEdge(dut.pdm_pulse)
        start_on = get_sim_time(TIME_UNIT)
        await FallingEdge(dut.pdm_pulse)
        start_off = get_sim_time(TIME_UNIT)
        await RisingEdge(dut.pdm_pulse)
        end_off = get_sim_time(TIME_UNIT)

        min_off = int(dut.min_off.value)
        max_on = int(dut.max_on.value)

        # - calculate on-time in cycles
        duration_on = start_off - start_on
        duration_off = end_off - start_off
        cycles_on = duration_on // CLOCK_PERIOD
        cycles_off = duration_off // CLOCK_PERIOD

        # - apply checks
        assert (
            cycles_on <= max_on + 1
        ), f"On-time is longer than max_on={max_on} cycles"
        assert (
            cycles_off >= min_off
        ), f"Off-time is shorter than min_off={min_off} cycles"

async def check_mea_ack(dut):
    dut._log.info("Starting `check_mea_ack()`...")

    # Inner assertion loop
    while True:
        # Make sure that the loop is activated at
        # the rising edge of `mea_req`
        await RisingEdge(dut.mea_req)
        start_r = get_sim_time(TIME_UNIT)

        # - wait for `mea_ack`
        await RisingEdge(dut.mea_ack)
        end_r = get_sim_time(TIME_UNIT)

        # - calculate wait time in cycles
        duration_r = end_r - start_r
        cycles_r = duration_r // CLOCK_PERIOD

        # - apply checks
        #assert int(dut.pdm_pulse.value) == 0, "Acknowledge flag asserted during a pulse"
        #assert cycles_r <= 2, "Acknowledge flag asserted too late"

        # Wait until `mea_req` and `mea_ack` are de-asserted
        await FallingEdge(dut.mea_req)
        start_f = get_sim_time(TIME_UNIT)
        await FallingEdge(dut.mea_ack)
        end_f = get_sim_time(TIME_UNIT)

        # - calculate wait time in cycles
        duration_f = end_f - start_f
        cycles_f = duration_f // CLOCK_PERIOD

        # - apply checks
        assert cycles_f <= 2, "Acknowledge flag de-asserted too late"


@cocotb.test()
async def main_test(dut):
    dut._log.info("Starting testing...")

    # Start sub-processes
    cocotb.start_soon(check_pulse_width(dut))
    cocotb.start_soon(check_mea_ack(dut))

    # - start stimulus generator, then wait for it
    await cocotb.start_soon(stimuli_generator(dut))

    dut._log.info("Testing done. All tests passed")
