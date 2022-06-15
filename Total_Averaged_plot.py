from labjack import ljm
import sys
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from windfreak import SynthHD
import time

def get_avg(intensities):
    avg = sum(intensities)/len(intensities)
    return avg 

def normalize(intensities):
    max_val = max(intensities)
    norm_vals = []
    for values in intensities:
        newval= values/max_val
        norm_vals.append(newval)
    return norm_vals
    
def average_arrays(arrs):
    nump_arrs= []
    for arrays in arrs:
        nump_arrs.append(np.array(arrays))
    
    avg= sum(nump_arrs)/ len(nump_arrs)
    return avg

print("\t \t \t \t Qubit initialization Process; Averaged ODMR Plot \n \n")

print("\t \t Initializing Systems \n \n")

#Labjack initialization 
handle = ljm.openS("ANY", "ANY", "ANY")
names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX", "AIN0_SETTLING_US",
             "AIN1_NEGATIVE_CH", "AIN1_RANGE", "AIN1_RESOLUTION_INDEX", "AIN1_SETTLING_US"]
aValues = [199, 10.0, 0, 0, 199, 10.0, 0, 0]
num_Frames= len(names)
ljm.eWriteNames(handle, num_Frames, names, aValues)
numFrames = 2
names = ["AIN0", "COD1"]
intervalHandle = 1
loopAmount = 1000 #for number of points collected per frequency

#Microwave VCO initialization
synth = SynthHD("COM3")
synth.init()
synth[0].power= 10.0
#synth[0].enable = True

print("\t \t Set Parameters \n \n")

start_frequency = int(float(input("Enter the starting frequency in GHz")) * 1e9)
stop_frequency = int(float(input("Enter the stop frequency in GHz: ")) * 1e9)
step_size = int(float(input("Enter the step size in MHz: "))* 1e6)
step_time = int(input("enter step time in microseconds: "))
num_plots = int(input("Enter number of plots to be averaged"))


#Plot Averaging System

count=1
intensity_list=[]
while count< num_plots+1:
    vals = {
        "Frequency":[],
        "Intensity":[]
    }

    for i in range(start_frequency, stop_frequency, step_size):
        ljm.startInterval(intervalHandle, step_time)
        synth[0].frequency = i
        j=0
        temp_intensity=[]
        while True:
            try:
                results = ljm.eReadNames(handle, numFrames, names)
                temp_intensity.append(results[0])
                ljm.waitForNextInterval(intervalHandle)
                if loopAmount != "infinite":
                    j=j+1
                    if j>= loopAmount:
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
    intensity_list.append(vals["Intensity"])
    
    df= pd.DataFrame(vals)
    normalized_intensities= normalize(vals["Intensity"])
    plt.plot(df['Frequency'], normalized_intensities)
    plt.xlabel("Frequency")
    plt.ylabel("Intensity")
    plt.title("Intensity vs Frequency Graph")
    title_string= str("Plot_number_"+ str(count))
    plt.savefig(title_string)
    print("Plot number ", count, " is generated")
    count=count+1




final_vals= {
    "Intensity":[],
    "Frequency":[]
}

for i in range(start_frequency, stop_frequency, step_size):
    final_vals["Frequency"].append(i)


final_intensity_vals= average_arrays(intensity_list)

normalized_intensities= normalize(final_intensity_vals)
df= pd.DataFrame(final_vals)

plt.plot(df["Frequency"], normalized_intensities)
plt.xlabel("Frequency")
plt.ylabel("Intensity")
plt.title("Intensity vs Frequency Graph")
plt.show()
plt.savefig("Averaged_Plot1")




