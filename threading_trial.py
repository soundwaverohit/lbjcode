import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from labjack import ljm
import os
import sys
import time
from threading import Timer


"""HELPER FUNCTIONS"""
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False



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


print('\n \n')
print("\t \t \t Spin-Relaxation T1 Time Measurement Protocol \n \n \n")


vals= {
    "Interval_Time":[],
    "Intensity": []
}

start_time= time.time()

handle = ljm.openS("ANY", "ANY", "ANY")
names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX", "AIN0_SETTLING_US",
             "AIN1_NEGATIVE_CH", "AIN1_RANGE", "AIN1_RESOLUTION_INDEX", "AIN1_SETTLING_US"]
aValues = [199, 10.0, 0, 0, 199, 10.0, 0, 0]
num_Frames= len(names)
ljm.eWriteNames(handle, num_Frames, names, aValues)
numFrames = 2
names = ["AIN0", "DAC0"]
intervalHandle = 1
loopAmount = 4000

ljm.startInterval(intervalHandle, 1)

i=0
while True:
    try: 
        results = ljm.eReadNames(handle, numFrames, names)
        vals["Interval_Time"].append(i)
        vals["Intensity"].append(results[0])
        ljm.waitForNextInterval(intervalHandle)
        if loopAmount is not 'infinte':
            i =i +1
            if i >= loopAmount:
                break
    except KeyboardInterrupt:
        break

    except Exception:
        print(sys.exc_info()[1])
        break


ljm.cleanInterval(intervalHandle)
ljm.close(handle)

stop_time= time.time()

if len(vals["Intensity"]) != len(vals["Interval_Time"]):
    print("THe values are unequal and therefore cannot be compiled or formatted properly")


df= pd.DataFrame(vals)
df.to_csv('SpinT1Time_Measurement_Trial_1.csv')

print("Total time to compile: ", stop_time- start_time)

plt.plot(vals["Interval_Time"], vals["Intensity"])
plt.xlabel("Time (in terms of microseconds)")
plt.ylabel("Intensity")
plt.title("Spin T1 Relaxation time measurement")
plt.savefig("SpinT1Time_Measurement_Trial_1")
plt.show()

