# -*- coding: UTF-8 -*-

#Python module requirement: line-bot-sdk, flask
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi('line_bot_api') #LineBot's Channel access token
handler = WebhookHandler('handler')        #LineBot's Channel secret
user_id_set=set()                                         #LineBot's Friend's user id 
app = Flask(__name__)

import time, DAN, requests, random, queue
import threading

ServerURL = 'http://140.113.199.195' #with no secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = '124jfas' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Line0516312'
DAN.profile['df_list']=['msgI', 'msgO']
DAN.profile['d_name']= None # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)


def job():
    while 1:
        value1 = DAN.pull('msgO')
        if value1!=None:
            try:
                for userId in user_id_set:
                    line_bot_api.push_message(userId, TextSendMessage(text=value1[0]))  # Push API example
            except Exception as e:
                print(e)
        #line_bot_api.push_message(userId, TextSendMessage(text=value1[0]))
        #time.sleep(1)



def loadUserId():
    try:
        idFile = open('idfile', 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None


def saveUserId(userId):
        idFile = open('idfile', 'a')
        idFile.write(userId+';')
        idFile.close()


@app.route("/", methods=['GET'])
def hello():
    return "HTTPS Test OK."

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']    # get X-Line-Signature header value
    body = request.get_data(as_text=True)              # get request body as text
    print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)                # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global value1
    Msg = event.message.text
    if Msg == 'Hello, world': return
    print('GotMsg:{}'.format(Msg))
    DAN.push('msgI',Msg)
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=value1))   # Reply API example
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text="收到訊息!!"))

    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)

   
if __name__ == "__main__":

    idList = loadUserId()
    if idList: user_id_set = set(idList)
    th = threading.Thread(target=job)
    th.daemon = True     # this ensures thread ends when main process ends
    th.start()
    try:
        for userId in user_id_set:
            line_bot_api.push_message(userId, TextSendMessage(text='LineBot is ready for you.'))  # Push API example
    except Exception as e:
        print(e)
    
    app.run('127.0.0.1', port=32768, threaded=True, use_reloader=False)
    
    

