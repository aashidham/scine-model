import math
import subprocess

import the_platform


def transient_analysis(circuit_fn, transient_step, transient_max_T):

    # Run the transient analysis.
    data = the_platform.file('the.data')
    inp = """
tran %f %f
wrdata '%s' electrode_bus solution_bus cell_bus
quit
""" % (transient_step, transient_max_T, '.'.join(data.split('.')[:-1]))
    subprocess.Popen(['ngspice', '-p', circuit_fn], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True).communicate(inp)

    # Plot <t> <voltage at electrode_bus>.
    plot_fn = the_platform.file('plot.png')
    subprocess.check_call("gnuplot -e \"set term png; set output '%s'; plot '%s' using 1:2 with linespoints\"" % (plot_fn, data), shell=True)

    return [data, plot_fn]


def ac_analysis(circuit_fn, exponent_low, exponent_high):

    # Run the AC analysis.
    data = the_platform.file('the.data')
    f_low = math.pow(10, exponent_low)
    f_high = math.pow(10, exponent_high)
    inp = """
ac dec %f %f %f
wrdata '%s' mag(electrode_bus) phase(electrode_bus)
quit
""" % (exponent_high - exponent_low, f_low, f_high, '.'.join(data.split('.')[:-1]))
    subprocess.Popen(['ngspice', '-p', circuit_fn], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True).communicate(inp)

    # Plot <f> <gain at electrode_bus>, and <f> <phase at electrode_bus>.
    mag_plot_fn = the_platform.file('plot-mag.png')
    subprocess.check_call("gnuplot -e \"set term png; set output '%s'; set logscale x; plot '%s' using 1:2 with linespoints\"" % (mag_plot_fn, data), shell=True)
    phase_plot_fn = the_platform.file('plot-phase.png')
    subprocess.check_call("gnuplot -e \"set term png; set output '%s'; set logscale x; plot '%s' using 3:4 with linespoints\"" % (phase_plot_fn, data), shell=True)

    return [data, mag_plot_fn, phase_plot_fn]
