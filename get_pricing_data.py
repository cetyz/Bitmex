# -*- coding: utf-8 -*-
"""
Created on Fri May  3 20:37:32 2019

@author: Cetyz
"""

#import bitmex
import requests
import csv
import pandas as pd
import os
from datetime import datetime
import json

myKeysJson = 'keys.json'
with open(myKeysJson, 'r') as f:
    myKeys = json.load(f)
    
myKey, secretKey = myKeys['api_key'], myKeys['api_secret']

living_csv = os.getcwd()+'\living_data.csv'

base_url = r'https://testnet.bitmex.com/api/v1'

def getOrderBook(symbol, depth = 1):
    params = {
            'symbol': str(symbol),
            'depth': str(depth),
            }
    response = requests.get(base_url + '/orderBook/L2', params).json()
    return(response)

def getVolume24hr(symbol):
    params = {
            'symbol': str(symbol),
            'columns': 'volume24h',
            'count': '1',
            }
    response = requests.get(base_url + r'/instrument', params = params).json()
    return(response[0]['volume24h'])

current_second = datetime.now().second

write_header = False
if write_header:
    with open(living_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ['Datetime', 'SellPrice', 'SellSize', 'BuyPrice', 'BuySize', 'Volume24h']
        writer.writerow(header)

jsonError = False    
while True:
    if datetime.now().second % 5 == 0:
        jsonError = False
        now = datetime.now()
        try:
            orderBook = getOrderBook('XBT', 1)
        except:
            print('Error getting orderbook at ' + str(now))
            jsonError = True
        try:
            volume24h = getVolume24hr('XBTUSD')
        except:
            print('Error getting 24h volume at ' + str(now))
            jsonError = True
        if not jsonError:
            sell_price = orderBook[0]['price']
            sell_size = orderBook[0]['size']
            buy_price = orderBook[1]['price']
            buy_size = orderBook[1]['size']
            with open(living_csv,'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([now, sell_price, sell_size, buy_price, buy_size, volume24h])
                print('Price added at ' + str(now))
            try:
                df = pd.read_csv(living_csv)
                df.to_csv('data.csv', index = False)
            except PermissionError:
                print('Data csv opened, data not copied over.')
#        current_second = now.second
    













#client = bitmex.bitmex(api_key = myKey, api_secret = secretKey)
#result = client.Order.Order_new(symbol='XBTUSD', orderQty=10, price = 1000).result()
#print(result)
#orderID = result[0]['orderID']
#print(orderID)
#time.sleep(5)
#result = client.Order.Order_cancel(orderID=str(orderID)).result()
#print(result)





#
#def postLimitOrder(symbol='XBTUSD', side='Buy', orderQty = '1',
#                   price = '0', ordType='Limit'):
#    if price == '0':
#        raise ValueError('Please indicate price')
#    params = {
#            'id': myKey,
#            'secret': secretKey,
#            'symbol': str(symbol),
#            'side': str(side),
#            'orderQty': str(orderQty),
#            'price': str(price),
#            'ordType': str(ordType),
#            }
#    
#    response = requests.post(base_url+'/order', json = params)
#    print(response.json())
#
#postLimitOrder(orderQty=10, price=10000)