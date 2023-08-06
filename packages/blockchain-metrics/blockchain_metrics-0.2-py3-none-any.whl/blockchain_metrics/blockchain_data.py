#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 21:48:59 2021
@author: juannM
"""

import matplotlib.pyplot as plt
import pandas as pd
import requests


def prefunction(name_type):
    
     url = 'https://api.blockchain.info/charts/'
     url = url+name_type
     payload = {'timespan'  : 'all','format':'json'}
     response = requests.get(url,params=payload)
     data = response.json()
     df = pd.DataFrame(data['values'])
     df.rename(columns={'y':data['name']},inplace = True)
     df['x'] = pd.to_datetime(df['x'],unit='s')
     df['timestamp'] = df['x'].dt.strftime('%Y-%m-%d')
     df.drop('x',inplace=True,axis=1)
     data = df
     return data
 
    
def prefunction_pool():
    
     url = 'https://api.blockchain.info/pools'
     days_pool = '7days'
     payload = {'timespan'  : days_pool,'format':'json'}
     response = requests.get(url,params=payload)
     data = response.json()
     df = pd.DataFrame([[key, data[key]] for key in data.keys()], columns=['Minner_Name', 'Blocks_mined'])
     return df
    
    
def prefunction_stats():
    
     url = 'https://api.blockchain.info/stats'
     days_pool = 'all'
     payload = {'timespan'  : days_pool,'format':'json'}
     response = requests.get(url,params=payload)
     data = response.json()
     df = pd.DataFrame([[key, data[key]] for key in data.keys()], columns=['Stat-Name', 'Value-mined'])
     return df
       
    
def prefunction_latstblock():
    
     url = 'https://blockchain.info/latestblock'
     payload = {'timespan'  : 'all','format':'json'}
     response = requests.get(url,params=payload)
     data = response.json()
     df = pd.DataFrame([[key, data[key]] for key in data.keys()], columns=['Stat-Name', 'Value-mined'])
     return df
       
    
def prefunction_balance_tx(tx_public):
    
     url = 'https://blockchain.info/balance?active='+tx_public
     payload = {'timespan'  : 'all','format':'json'}
     response = requests.get(url,params=payload)
     data = response.json()
     df = pd.DataFrame([[key, data[key]] for key in data.keys()], columns=['Stat-Name', 'Value-mined'])
     return df
    
    
def tickers_fiat():
    
     url = 'https://blockchain.info/es/ticker'
     payload = {'timespan'  : 'all','format':'json'}
     response = requests.get(url,params=payload)
     data = response.json()
     df = pd.DataFrame([[key, data[key]] for key in data.keys()], columns=['Symbol-fiat', 'Value-mined'])
     return df


class blockchain_stats_currency:
    
    def __init__(self):
        

        self.preload = None
        self.var_url = None
        self.colum = None
        
        
    def total_bitcoins(self):
        
         var = 'total-bitcoins'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload
    
    def market_price(self):
        
        var = 'market-price'
        self.var_url = var
        self.preload = prefunction(var)
        self.colum = self.preload.columns[0]
        return self.preload
    
    def market_cap(self):
        
        var = 'market-cap'
        self.var_url = var
        self.preload = prefunction(var)
        self.colum = self.preload.columns[0]
        return self.preload
    
    def trade_volume(self):
        
        var = 'trade-volume'
        self.var_url = var
        self.preload = prefunction(var)
        self.colum = self.preload.columns[0]
        return self.preload
    
    def blocks_size(self):
        
         var = 'blocks-size'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload
    
    def avg_block_size(self):
        
        var = 'avg-block-size'
        self.var_url = var
        self.preload = prefunction(var)
        self.colum = self.preload.columns[0]
        return self.preload
    
    def n_transactions_per_block(self):
        
        var = 'n-transactions-per-block'
        self.var_url = var
        self.preload = prefunction(var)
        self.colum = self.preload.columns[0]
        return self.preload
    
    def n_transactions_total(self):
        
        var = 'n-transactions-total'
        self.var_url = var
        self.preload = prefunction(var)
        self.colum = self.preload.columns[0]
        return self.preload
    
    def median_confirmation_time(self):
        
        var = 'median-confirmation-time'
        self.var_url = var
        self.preload = prefunction(var)
        self.colum = self.preload.columns[0]
        return self.preload
    
    def avg_confirmation_time(self):
        
        var = 'avg-confirmation-time'
        self.var_url = var
        self.preload = prefunction(var)
        self.colum = self.preload.columns[0]
        return self.preload
       
    
    def hash_rate(self):
        
         var = 'hash-rate'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload
    
    
    def difficulty(self):
        
         var = 'difficulty'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload
     
        
    def miners_revenue(self):
        
         var = 'miners-revenue'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload   
     
    
    def transaction_fees(self):
        
         var = 'transaction-fees'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload

    def transaction_fees_usd(self):
        
         var = 'transaction-fees-usd'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload
    
    def cost_per_transaction_percent(self):
        
         var = 'cost-per-transaction-percent'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload
     
    def cost_per_transaction(self):
        
         var = 'cost-per-transaction'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload  
        
    def n_unique_addresses(self):
        
         var = 'n-unique-addresses'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload
    
    
    def n_transactions(self):
        
         var = 'n-transactions'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload
     
    
    def transactions_per_second(self):
        
         var = 'transactions-per-second'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload

    def output_volume(self):
        
         var = 'output-volume'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload
     
    def mempool_count(self):
        
         var = 'mempool-count'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload
     
    def mempool_growth(self):
        
         var = 'mempool-growth'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload
     
    def mempool_size(self):
        
         var = 'mempool-size'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload  
    
    def utxo_count(self):
        
         var = 'utxo-count'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload  
     
    def n_transactions_excluding_popular(self):
        
         var = 'n-transactions-excluding-popular'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload  
     
        
    def estimated_transaction_volume(self):
        
         var = 'estimated-transaction-volume'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload  
     
    def estimated_transaction_volume_usd(self):
        
         var = 'estimated-transaction-volume-usd'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload  
     
    def my_wallet_n_users(self):
        
         var = 'my-wallet-n-users'
         self.var_url = var
         self.preload = prefunction(var)
         self.colum = self.preload.columns[0]
         return self.preload
     
    def pools(self):
        
        self.preload = prefunction_pool()
        return self.preload
        
    def stats(self):
        
        self.preload = prefunction_stats()
        return self.preload
     
    def plot_data(self):
        
        plt.figure(figsize=(12,5))
        plt.title('Time series of ' + str(self.var_url))
        plt.xlabel('Time')
        plt.ylabel(str(self.var_url))
        ax = plt.gca()
        ax1 = self.preload.plot(kind='line' ,x = 'timestamp' , y=self.colum ,ax=ax, grid=True,color='blue',label=str(self.var_url))
        ax1.legend(loc=2)
        plt.show()

    def plot_pools_pie(self):
        plt.figure(figsize=(10,20))
        minner_name = self.preload['Minner_Name'].tolist()
        blocks_mined = self.preload['Blocks_mined'].tolist()
        plt.pie(blocks_mined,labels=minner_name,autopct="%0.1f %%")
        plt.show()
        
        
        
        
        
        
        
        