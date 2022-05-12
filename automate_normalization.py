from labjack import ljm
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from windfreakpython.windfreak import SynthHD



print("\t \t \t \t ODMR Multiple Read Process; ODMR Plot \n \n")

print("\t \t Initializing Systems \n \n")


synth = SynthHD('COM3')
handle = ljm.openS("ANY", "ANY", "ANY")
names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX", "AIN0_SETTLING_US",
             "AIN1_NEGATIVE_CH", "AIN1_RANGE", "AIN1_RESOLUTION_INDEX", "AIN1_SETTLING_US"]
aValues = [199, 10.0, 0, 0, 199, 10.0, 0, 0]
num_Frames= len(names)
ljm.eWriteNames(handle, num_Frames, names, aValues)
numFrames = 2
names = ["AIN0", "COD1"]
loopAmount=1000
intervalHandle=1
vals = {
    "Frequency": [],
    "Intensity": []
}

print("\t \t Set Parameters \n \n")

start_frequency = int(2.8 * 1e9)
stop_frequency = int(2.9* 1e9)
step_size = int(1 * 1e6)
step_time = int(1)


def get_avg(intensities):
    avg = sum(intensities)/ len(intensities)
    return avg


def normalize(intensities):
    max_val = max(intensities)
    norm_vals = []
    for values in intensities:
        newval= values/max_val
        norm_vals.append(newval)
    return norm_vals



synth.init()
synth[0].power = 10.0


num_plots= int(input("Enter the number of plots to run: "))


for plots in range(num_plots):
    plot_num=1

    print("INPUT VALUES ITERATION NUMBER: ", plot_num)
    print("Parameters are: ", start_frequency,stop_frequency, step_size, step_time)



    for i in range(start_frequency, stop_frequency, step_size):
        ljm.startInterval(intervalHandle, step_time) 
        j=0 
        temp_intensity=[]

        while True:
            try:
                results = ljm.eReadNames(handle, numFrames, names)
                temp_intensity.append(results[0])
                ljm.waitForNextInterval(intervalHandle)
                if loopAmount != "infinite":
                    j=j+1
                    if j >= loopAmount:
                        break
            except KeyboardInterrupt:
                break
            except Exception:
                print(sys.exc_info()[1])
                break
        vals["Intensity"].append(get_avg(temp_intensity))
        vals["Frequency"].append(i)
        ljm.cleanInterval(intervalHandle)
        ljm.close(handle)
        string = str("Frequency ", i, " is set and intensity data values collected ", loopAmount, " times")
        print(string)
        df= pd.DataFrame(vals)
        normalized_intensities= normalize(vals["Intensity"])

        stringsave= str("Iteration_"+str(plot_num)+"_plot")

        plt.plot(df['Frequency'], normalized_intensities)
        plt.xlabel("Frequency")
        plt.ylabel("Intensity")
        plt.title("Intensity vs Frequency Graph")
        plt.savefig(stringsave)

        plot_num= plot_num+1


        print("\n \n \t STARTING ITERATION NUMBER: ", plot_num )


