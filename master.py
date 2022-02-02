from labjack import ljm
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation



""" CODE FOR WINDFREAK FREQUENCY GENERATOR AND IDENTIFIER """
from windfreakpython.windfreak import SynthHD
synth = SynthHD('/dev/ttyACM0')
synth.init()
# Set channel 0 power and frequency
synth[0].power = -10.
synth[0].frequency = 2.e9
# Enable channel 0
synth[0].enable = True


""" CODE FOR LABJACK FOR READING INTENSITY FROM THE PHOTODIODE"""
handle = ljm.openS("ANY", "ANY", "ANY")  # Any device, Any connection, Any identifier

def read_voltage(name):
    result = ljm.eReadName(handle,name)
    return result

# above function reads the voltage recieved from a specific register on the labjack.

#sample implementation
loopAmount = 10
loopMessage = " Press Ctrl+C to stop."
names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX", "AIN0_SETTLING_US",
             "AIN1_NEGATIVE_CH", "AIN1_RANGE", "AIN1_RESOLUTION_INDEX", "AIN1_SETTLING_US"]
             
aValues = [199, 10.0, 0, 0, 199, 10.0, 0, 0]
num_Frames= len(names)
ljm.eWriteNames(handle, num_Frames, names, aValues)
for i in range(num_Frames):
    print("    %s : %f" % (names[i], aValues[i]))


# Read AIN0 and AIN1 from the LabJack with eReadNames in a loop.
numFrames = 2
names = ["AIN0", "AIN1"]

#storing the values of read voltages from the analog inputs in the labjack
vals= {
    "AIN0": [],
    "AIN1": []
}

xpts=[]
ypts= []
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

frequencies= []
voltages= []


#function to generate the frequencies based on the windfreak inputted values
def frequency_generator():
    frequency= 1
    return frequency



print("\nStarting %s read loops.%s\n" % (str(loopAmount), loopMessage))
intervalHandle = 1
ljm.startInterval(intervalHandle, 1000000)  # Delay between readings (in microseconds)
i = 0
while True:
    try:
        results = ljm.eReadNames(handle, numFrames, names)
        #print("AIN0 : %f V, AIN1 : %f V" % (results[0], results[1]))
        vals["AIN0"].append(results[0])
        vals["AIN1"].append(results[1])
        ljm.waitForNextInterval(intervalHandle)
        df= pd.DataFrame(vals)
        def animate(i, xpts, ypts):
            xpts.append(results[0])
            ypts.append(results[1])
            ax.clear()
            ax.plot(xpts, ypts)
            plt.xticks(rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.30)
            plt.title('Frequency vs intensity')
            plt.xlabel('Frequncy')
            plt.ylabel('Intensity')
        
        ani= animation.FuncAnimation(fig, animate, fargs=(xpts,ypts), interval =1)
        plt.show()
    
        if loopAmount is not "infinite":
            i = i + 1
            if i >= loopAmount:
                break
    except KeyboardInterrupt:
        break
    except Exception:
        print(sys.exc_info()[1])
        break

print(df) #the voltage values from the analog inputs in a dataframe

"""
The above code is to read the voltages in real time from the analog channels and now the below code will be
about graphing the voltages top intensity
"""

# Close handles
ljm.cleanInterval(intervalHandle)
ljm.close(handle)


#plt.plot(xpts, ypts)
#plt.show()


