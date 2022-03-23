from labjack import ljm
import sys
import pandas as pd
import matplotlib.pyplot as plt
from windfreakpython.windfreak import SynthHD


print("\t \t \t \t Qubit initialization Process; ODMR Plot \n \n")


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

start_frequency = int(float(input("Enter the starting frequency in GHz")) * 1e9)
stop_frequency = int(float(input("Enter the stop frequency in GHz: ")) * 1e9)
step_size = int(float(input("Enter the step size in MHz: "))* 1e6)
step_time = int(input("enter step time in microseconds: "))


def get_avg(intensities):
    avg = sum(intensities)/ len(intensities)
    return avg


for i in range(start_frequency, stop_frequency, step_size):
    ljm.startInterval(intervalHandle, step_time)  
    synth.init()
    synth[0].power = 10.0
    synth[0].frequency = i
    synth[0].enable = True
    j=0
    temp_intensity = []

    while True:
        try:
            results = ljm.eReadNames(handle, numFrames, names)            
            temp_intensity.append(results[0])
            ljm.waitForNextInterval(intervalHandle)
            if loopAmount != "infinite":
                j =j +1
                if j >= loopAmount:
                    break
        except KeyboardInterrupt:
            break
        except Exception:
            print(sys.exec_inf()[1])
            break
    vals["Intensity"].append(get_avg(temp_intensity))
    vals["Frequency"].append(i)
    ljm.cleanInterval(intervalHandle)
    ljm.close(handle)
    string = str("Frequency ", i, " is set and intensity data values collected ", loopAmount, " times")
    print(string)

df= pd.DataFrame(vals)
#print(df)

plt.plot(df['Frequency'], df['AIN0'])
plt.xlabel("Frequency")
plt.ylabel("Intensity")
plt.title("Intensity vs Frequency Graph")
plt.show()
