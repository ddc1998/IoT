import random
import time

from dan import NoData

### The register server host, you can use IP or Domain.
host = 'iottalk2.tw'

### [OPTIONAL] The register port, default = 9992
# port = 9992

### [OPTIONAL] If not given or None, server will auto-generate.
# device_name = 'Dummy_Test'

### [OPTIONAL] If not given or None, DAN will register using a random UUID.
### Or you can use following code to use MAC address for device_addr.
# from uuid import getnode
# device_addr = "{:012X}".format(getnode())
#device_addr = "aa8e5b58-8a9b-419b-b8d5-72624d61108d"

### [OPTIONAL] If not given or None, this device will be used by anyone.
username = 'None'

### The Device Model in IoTtalk, please check IoTtalk document.
device_model = 'Dummy_Device'

### The input/output device features, please check IoTtalk document.
idf_list = ['Dummy_Sensor']
odf_list = ['Dummy_Control']

### Set the push interval, default = 1 (sec)
### Or you can set to 0, and control in your feature input function.
push_interval = 10  # global interval
interval = {
    'Dummy_Sensor': 0.1,  # assign feature interval
}
def register_callback():
    print('register successfully')
lasttime = 0
cnt = 0
sum_delay = 0
avg_delay = 0

def Dummy_Sensor():
    nowtime = time.time()
    return nowtime
    # return NoData

def Dummy_Control(data):  # data is a list
    global cnt, sum_delay, avg_delay
    if(cnt >= 100):    
        avg_delay = sum_delay/100
        print('avg_delay = ')
        print(avg_delay)
    if(cnt < 100):
        cnt = cnt+1
        delta = time.time() - data[0]
        sum_delay = sum_delay + delta
        print(delta)
    #time.sleep(0.1)