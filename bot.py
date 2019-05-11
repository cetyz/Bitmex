# -*- coding: utf-8 -*-
"""
Created on Mon May  6 22:23:49 2019

@author: Cetyz
"""

import requests
import time
import hmac
import hashlib
import json
import algo # my own script
import pandas as pd
from datetime import datetime

'''
The bot's general strategy:
    
every 5 seconds,
check to see if the future price (1 min in the future) is higher or lower
if higher, market buy, if lower, market sell. maybe a $2 threshold?
if there is a position open, do not add any new positions
when the 1 min mark comes, close the position
then start waiting to open a new one when a new threshold is reached
'''

myKey = 'rm9nCbmrnxQLGOxl-vA0kW1R'
secretKey = 'muCtiYLUBzexGPaf52Dl3ViKfS7QT0o_j6nnj421Ch7n78ko'

waitingToBuy = False
waitingToSell = False
global lastOrderTime
lastOrderTime = None

def buy():
    
    base_url = 'https://testnet.bitmex.com' ###
    verb = 'POST'
    
    data = {"symbol":"XBTUSD","orderQty":10,"ordType":"Market"} ### side?
    
    f_url = '/api/v1/order'
    url = base_url + f_url
    expires = int(round(time.time()) + 5) ###
    
    message = verb + f_url + str(expires) + json.dumps(data) ###
    
    signature = hmac.new(bytes(secretKey, 'utf-8'), bytes(message, 'utf-8'), digestmod=hashlib.sha256).hexdigest() ###
    
    headers = {'api-expires':str(expires),'api-key':myKey,'api-signature':signature}
    r = requests.post(url, headers=headers, json=data).json() ###
    global lastOrderTime
    lastOrderTime = datetime.now()
#    print(r)
    print('Made a BUY at ' + str(r['price']))
    
def sell():
    
    base_url = 'https://testnet.bitmex.com' ###
    verb = 'POST'
    
    data = {"symbol":"XBTUSD","orderQty":-10,"ordType":"Market"} ### side?
    
    f_url = '/api/v1/order'
    url = base_url + f_url
    expires = int(round(time.time()) + 5) ###
    
    message = verb + f_url + str(expires) + json.dumps(data) ###
    
    signature = hmac.new(bytes(secretKey, 'utf-8'), bytes(message, 'utf-8'), digestmod=hashlib.sha256).hexdigest() ###
    
    headers = {'api-expires':str(expires),'api-key':myKey,'api-signature':signature}
    r = requests.post(url, headers=headers, json=data).json() ###
    global lastOrderTime
    lastOrderTime = datetime.now()
    print('Made a SELL at ' + str(r['price']))
#    print(r)

while True:
    if datetime.now().second % 5 == 0:
        if (not waitingToBuy) and (not waitingToSell):
            # train the model
            df_to_train = algo.process()
            model = algo.Model(df_to_train)
            
            df_to_predict = algo.process(forBotUse=True)
            targetRow = df_to_predict.iloc[-1, :]
            try:
                prediction = model.model.predict(targetRow.values.reshape(1, -1))[0]
            except ValueError:
                print('Error making prediction. targetRow might contain infinity or NaN')
                print('Setting prediction to current price.')
                prediction = targetRow.get('Price-0')
            print('Current price is:', targetRow.get('Price-0'))
            print('Price predicted to be ' + str(prediction) + ' in 1 min\'s time')
            if (prediction - targetRow.get('Price-0')) > 2:
                buy()
                waitingToSell = True
            elif (targetRow.get('Price-0') - prediction) > 2:
                sell()
                waitingToBuy = True
            else:
                print('Waiting to make a move...')
                time.sleep(1)
            print('')

        
        elif waitingToBuy:
            while True:
                if (datetime.now() - lastOrderTime).total_seconds() >= 60:
                    buy()
                    waitingToBuy = False
                    break
    #            else:
    #                if datetime.now().second % 5 == 0:
    #                    print('Waiting to close open short position')
                
        elif waitingToSell:
            while True:
                if (datetime.now() - lastOrderTime).total_seconds() >= 60:
                    sell()
                    waitingToSell = False
                    break
    #            else:
    #                if datetime.now().second % 5 == 0:
    #                    print('Waiting to close open long position')
            


    

