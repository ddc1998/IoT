import time, DAN, requests, random

ServerURL = 'http://140.113.199.195' #with no secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = None #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Dummy_Device'
DAN.profile['df_list']=['Dummy_Sensor', 'Dummy_Control']
DAN.profile['d_name']= None # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)

tag = 0
cnt = 0
now_time = 0
delta = 0
avg_delay = 0
sum_delay = 0

while True:
    try:
    #Pull data from a device feature called "Dummy_Control"
        DAN.push ('Dummy_Sensor',time.time())
        value1=DAN.pull('Dummy_Control')
        if cnt >= 100:
        	avg_delay = sum_delay/100
        	print(avg_delay)
        if value1 != None and cnt < 100:
            
            #if value1[0] == now_time
            delta = time.time() - value1[0]
            sum_delay = sum_delay + delta
            print(sum_delay)
            cnt = cnt + 1    
    #Push data to a device feature called "Dummy_Sensor"
        #value2=random.uniform(1, 10)
        
        #time.sleep(0.1)


    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    #time.sleep(0.2)

