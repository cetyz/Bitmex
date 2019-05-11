# -*- coding: utf-8 -*-
"""
Created on Tue May  7 01:30:16 2019

@author: Cetyz
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from datetime import datetime
from datetime import timedelta
import seaborn as sns
import matplotlib.pyplot as plt

## PARAMETERS ##
periods = 12
target = timedelta(hours=0, minutes=5, seconds=0) # how much timedelta in the future to predict

def process(forBotUse = False):

    data_path = 'data.csv'
    df = pd.read_csv(data_path)
    
    # change Datetime column to datetime format and remove nanoseconds
    df['Datetime'] = pd.to_datetime(df['Datetime']).astype('datetime64[s]')
    # get price, which is just buy price and sell price added together then divided
    df['Price'] = (df['SellPrice']+df['BuyPrice'])/2
    
    # get a column for prices 1 min in the future
    # start by creating a reference column to be the key to merge with later
    df['TargetDatetime'] = df['Datetime'] + target
    # create a new df with just time and price
    dfTemp = pd.concat([df['Datetime'], df['Price']], axis = 1)
    # rename the new columns
    dfTemp = dfTemp.rename(index = str, columns={'Datetime':'TargetDatetime',
                                                 'Price': 'TargetPrice'})
    # merge
    df = df.merge(dfTemp, how='left', on='TargetDatetime')       
    
#    df['SellPrice+1min'] = df.join(dfTemp, on=')
#    df['Price-0'] = (df['SellPrice']+df['BuyPrice'])/2
#    
#    
#    for period in range(1, periods+1):
#    
#        df['Price-'+str(period)] = df['Price-0'].shift(periods=period)
#    
#    # calculate RSI
#    df['Delta'] = (df['Price-0'].diff()/df['Price-1'])*100 # the change in %
#    df['dUp'], df['dDown'] = df['Delta'], df['Delta']
#    df['dUp'].mask(df['dUp'] < 0, 0, inplace = True)
#    df['dDown'].mask(df['dDown'] > 0, 0, inplace = True)
#    df['RolUp'] = df['dUp'].rolling(periods).mean()
#    df['RolDown'] = df['dDown'].rolling(periods).mean().abs()
#    df['RSI'] = 100 - (100 / (1 + (df['RolUp']/periods)/(df['RolDown']/periods)))
#    
#    
#    df['SellPrice+12'] = df['SellPrice'].shift(periods=-12)
#    df['BuyPrice+12'] = df['BuyPrice'].shift(periods=-12)
#    df['TargetPrice'] = (df['SellPrice+12']+df['BuyPrice+12'])/2
#    
#    columns_to_drop = ['Delta', 'dUp', 'dDown', 'RolUp', 'RolDown', 'SellPrice+12', 'BuyPrice+12']
    columns_to_drop = ['SellPrice', 'BuyPrice', 'TargetDatetime']
    df.drop(columns_to_drop, axis=1, inplace=True)
#    
    if not forBotUse:
        df = df.dropna()
    else:
        df.drop(['TargetPrice', 'Datetime'], axis = 1, inplace = True)
#    
    df.to_csv('test.csv', index=False)
    return(df)

class Model:
    def __init__(self, df):
        self.model = GradientBoostingRegressor()
        # decide whether to split data into train and test set
        if __name__ == '__main__':
            self.train_X, self.train_y, self.test_X, self.test_y = self.prepare(df)
        # or to use all the available data
        else:
            self.train_X, self.train_y = self.prepare(df)
        self.train(self.train_X, self.train_y)
        
    def prepare(self, df):
        # i guess only use the last...... 5k cases? FOR NOW
        # work in to take current time, and maybe only consider data from the last 24hrs?
        # set one quarter of the cases aside for test dataset
        if __name__ == '__main__':
            df = df.iloc[-5000:, :]
            cutoff = int(df.shape[0]/4*3)
            
            train = df.iloc[:cutoff, :]
            test = df.iloc[cutoff:, :]
            
            train_X = train.drop(['TargetPrice', 'Datetime'], axis=1)
            train_y = train['TargetPrice']
            
            test_X = test.drop(['TargetPrice', 'Datetime'], axis=1)
            test_y = test['TargetPrice']
            
            return(train_X, train_y, test_X, test_y)
            
        else:
            train = df
            train_X = train.drop(['TargetPrice', 'Datetime'], axis=1)
            train_y = train['TargetPrice']
            
            return(train_X, train_y)
        
        
        
    def train(self, train_X, train_y):
        self.model.fit(train_X, train_y)
        
    def show_plot(self):
        if __name__ == '__main__':
            predictions = self.model.predict(self.test_X)
            g = sns.lineplot(x=range(self.test_y.shape[0]), y=self.test_y)
            plt.plot(predictions)
        else:
            print('Unable to show plot because all data is being used for training (no test set)')
 
    def show_MSE(self):
        if __name__ == '__main__':
            predictions = self.model.predict(self.test_X)
    
            results = pd.DataFrame()
            results['targets'] = self.test_y
            results['predictions'] = predictions
            results['residuals'] = results['targets'] - results['predictions']
            results['residuals_sq'] = results['residuals'] ** 2
            
            MSE = results['residuals_sq'].sum()/results.shape[0]
            print('MSE:', MSE)
        else:
            print('Unable to show MSE because all data is being used for training (no test set)')    
    
    

if __name__ == '__main__':
    df = process()

    model = Model(df)
    model.show_plot()
    model.show_MSE()
