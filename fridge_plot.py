import argparse, re, datetime

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import AutoMinorLocator

def fridge_plot(inpath, outpath, fs = 13):

    timestamp = []
    setpoint_deg = []
    fridge_temp_deg = []
    product_temp_deg = []
    
    with open(inpath, 'rb') as infile:
        for line in infile:
            line = line.decode("utf-8").strip()
            m = re.search("^(.+?): Set point: (.+?), fridge temp.: (.+?), product temp.: (.+?)$",
                          line)
            if not m:
                continue

            timestamp.append(datetime.datetime.strptime(m.group(1), "%a %b %d %H:%M:%S %Y"))
            setpoint_deg.append(float(m.group(2)))
            fridge_temp_deg.append(float(m.group(3)))
            product_temp_deg.append(float(m.group(4)))

    hours_elapsed = [(cur - timestamp[0]).total_seconds() / 3600 for cur in timestamp]
            
    fig = plt.figure(figsize = (5, 3.5), layout = "constrained")
    gs = GridSpec(1, 1, figure = fig)
    ax = fig.add_subplot(gs[0, 0])

    ax.plot(hours_elapsed, fridge_temp_deg, color = "black")

    ax.tick_params(axis = "y", direction = "in", which = "both", left = True, right = True, labelsize = fs)
    ax.tick_params(axis = "x", direction = "in", which = "both", bottom = True, top = True, labelsize = fs)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    
    ax.set_ylim(-70, 70)
    ax.set_xlabel("Time elapsed [hrs]", fontsize = fs)
    ax.set_ylabel(r"Chamber temperature [$\degree$C]", fontsize = fs)
    ax.axhline(-60, color = "gray", ls = "dashed", lw = 1)
    ax.axhline(60, color = "gray", ls = "dashed", lw = 1)
    
    fig.savefig(outpath)
    plt.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", action = "store", dest = "inpath")
    parser.add_argument("--outfile", action = "store", dest = "outpath")
    args = vars(parser.parse_args())

    fridge_plot(**args)
