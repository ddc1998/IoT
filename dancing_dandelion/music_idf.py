import time, os, sys, requests, random
import threading
import numpy as np
import pygame as pg
import DAN

ServerURL = 'http://140.113.199.195'  #with no secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = None  #if None, Reg_addr = MAC address

DAN.profile['dm_name'] = 'musicModel'
DAN.profile['df_list'] = ['musicMonitorI', 'musicMonitorO']
#DAN.profile['df_list'] = ['Sandy_I', 'Sandy_O']
DAN.profile['d_name'] = None  # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)

time_probe = 0  # global variable
last_time = 0  # global variable
now_time = 0  # global variable


def playMp3(music_file):
    # pick a midi or MP3 music file you have in the working folder
    # or give full pathname
    #music_file = "Drumtrack.mp3"

    freq = 44100  # audio CD quality
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 2048  # number of samples (experiment to get right sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    #pg.mixer.init()

    # optional volume 0 to 1.0
    pg.mixer.music.set_volume(0.8)

    # play music
    print("Playing...")
    clock = pg.time.Clock()
    pg.mixer.music.load(music_file)
    pg.mixer.music.play()
    # check if playback has finished
    while pg.mixer.music.get_busy():
        clock.tick(30)


# function: secToMin(turn the time info into second type)
# param: time_info(string type, ex: '1:02')
# retVal: minute(int type, ex: 68)
def secToMin(time_info):
    value = time_info.split(':')
    minute = int(value[0])
    second = int(value[1])
    minute = minute * 60 + second
    return minute


def job_of_play_music(music_file):
    def call():
        playMp3(music_file)

    p = threading.Thread(target=call)
    p.setDaemon(True)
    p.start()


def job_of_time_action_info(_action_list):
    global time_probe
    global last_time
    global now_time
    last_time = 0
    while (time_probe < len(action_list)):
        # get current action list
        target = action_list[time_probe]
        # get current time
        now_time = target[0]
        # iottalk delay
        #now_time -= 2
        # get current action
        target_action = target[1]
        target_time = now_time - last_time
        time.sleep(target_time)
        print("timer: ", end='')
        print(now_time)
        print("action: ", end='')
        print(target_action)
        #if (DAN.state == 'SET_DF_STATUS'):
        DAN.push('musicMonitorI', target_action)
        # update last_time
        last_time = now_time
        # move probe to next action
        time_probe += 1
    time.sleep(300)  # dummy delay XDD


if __name__ == '__main__':
    # read time and action info from file
    fp = open("lemon_action.txt", "r")
    # parsing input info
    # single_action[0] -> time_info(ex: '0:00')
    # single_actino[1] -> action_info(ex: '1')
    action_list = []
    for line in fp:
        single_action = line.strip().split(',')
        action_list.append([secToMin(single_action[0]), single_action[1]])
    # end of parsing
    fp.close()

    while (DAN.state != 'SET_DF_STATUS'):
        # wait for DAN ready
        time.sleep(0.1)
    # play music
    job_of_play_music("lemon.mp3")

    # play action
    job_of_time_action_info("lemon_action.txt")
