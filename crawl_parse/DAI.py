import time, DAN, requests, random
from bs4 import BeautifulSoup

ServerURL = 'http://140.113.199.200' #with no secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = None #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Dummy_Device'
DAN.profile['df_list']=['Dummy_Sensor', 'Dummy_Control']
DAN.profile['d_name']= None # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)

region = 'HsinChu' 
url = 'https://www.cwb.gov.tw/V7/observe/24real/Data/46757.htm'
df_tmp = None

def f(url, fn):
    headers = {
     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'

    #open(fn,'wb').write(res.text.encode('utf-8'))

    soup = BeautifulSoup(res.text, "lxml")
    global df_tmp
    df_tmp = get_element(soup, 'table','BoxTable')


def get_element(soup, tag, class_name):
    data = []
    table = soup.find(tag, attrs={'class':class_name})
    rows = table.find_all('tr')
    del rows[0]
    
    for row in rows:
        first_col = row.find_all('th')
        cols = row.find_all('td')
        cols.insert(0, first_col[0])
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) 
    return data

fn = region+ '.html'.format(0,0)
f(url, fn)


while True:
    try:
    #Pull data from a device feature called "Dummy_Control"
        value1=DAN.pull('Dummy_Control')
        if value1 != None:
            print (value1[0])

    #Push data to a device feature called "Dummy_Sensor"
        value2=random.uniform(1, 10)
        DAN.push ('Dummy_Sensor', df_tmp[0][1],  df_tmp[0][8])


    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)

