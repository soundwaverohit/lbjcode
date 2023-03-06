import time


test_arr=[]

start= time.time()
for i in range(4000):
    test_arr.append(i)
end= time.time()

print(end-start)