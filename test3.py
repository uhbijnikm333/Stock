# -*- coding: utf-8 -*-
"""
Created on Fri May  7 17:02:59 2021

@author: Ivan
課程教材：行銷人轉職爬蟲王實戰｜5大社群平台＋2大電商
版權屬於「楊超霆」所有，若有疑問，可聯絡ivanyang0606@gmail.com

第八章 shapee市場預估－這個市場有多大？
shapee爬蟲
"""
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
import json
import pygsheets
import pandas as pd

gc = pygsheets.authorize(service_account_file='credentials.json')
survey_url = 'https://docs.google.com/spreadsheets/d/12FAOEx69T3enW4F73kr1p4LmGUmDTnrqbbepF89LPlQ/edit#gid=0'
wb_key = gc.open_by_url(survey_url)
sh = wb_key.sheet1
Name = []
Shopid = []
Itemid = []
isNew = True

token = 'QmakjosRJ8YB9hUDjwuREtn7DRNK4GTqGLLxlsno0hX'
def searchNewItem(newItemid):
    isNew = True
    count = 0
    for passs in range(len(newItemid)):
        for i in range(len(Itemid)):
            print(f"newItemid[passs]['item_basic']['itemid'] : {newItemid[passs]['item_basic']['itemid']}")
            print(f"Itemid[i] : {Itemid[i]}")
            if newItemid[passs]['item_basic']['itemid']== Itemid[i]:
                count = count+1
                print(count)
                break
            else:
                if passs == len(Itemid):
                    message = "https://shopee.tw/product/"+str(newItemid[passs]['item_basic']['itemid'])+"/"+str(newItemid[passs]['item_basic']['shopid'])
                    result = lineNotifyMessage(token, message)
                    print(result)
                    WriteDataBase()
                    return True
               
    return True
                
            
        
def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token, # 權杖，Bearer 的空格不要刪掉呦
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    
    # Post 封包出去給 Line Notify
    r = requests.post(
        "https://notify-api.line.me/api/notify",
        headers=headers, 
        params=payload)
    return r.status_code

def WriteDataBase() :
    
    url = "https://shopee.tw/api/v4/search/search_items?by=ctime&keyword="+Keyword+"&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/111.26 (KHTML, like Gecko) Chrome/33.0.6785.145 Safari/666.11'}
    res = requests.get(url,headers=headers)
    data = res.json()['items']
    for i in range(len(data)):
        
        Name.append(1)
        Itemid.append(1)
        Shopid.append(1)
        Name[i] = data[i]['item_basic']['name']
        Shopid[i] = data[i]['item_basic']['shopid']
        Itemid[i] = data[i]['item_basic']['itemid']
        if i >=1000:
                sh.add_rows(1)
    df1 = pd.DataFrame(Name)
    sh.set_dataframe(df1, 'A1', copy_index=False, nan='')
    df1 = pd.DataFrame(Shopid)
    sh.set_dataframe(df1, 'B1', copy_index=False, nan='')
    df1 = pd.DataFrame(Itemid)
    sh.set_dataframe(df1, 'C1', copy_index=False, nan='')
    sh.cell('A1').value = 'Name'# -*- coding: utf-8 -*-
    sh.cell('B1').value = 'Itimid'
    sh.cell('C1').value = 'Shopid'
    sh.cell('D1').value = 'Ct'
    return len(data)
def ReadDataBase():
    user_df = sh.get_as_df(start='A2', index_colum=0, empty_value='', include_tailing_empty=False)
    return user_df
def MonitorGoods(CurrentLen,Keyword):
    while True:
        print('----正在等待新商品中----')
        url = "https://shopee.tw/api/v4/search/search_items?by=ctime&keyword="+Keyword+"&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/111.26 (KHTML, like Gecko) Chrome/33.0.6785.145 Safari/666.11'}
        res = requests.get(url,headers=headers)
        new_data = res.json()['items']
        if CurrentLen<len(new_data):
            print(f'Have a new goods')
            search = searchNewItem(new_data)
def ProudectURL():
    Keyword = input('請輸入想找的商品 :')  
    url
    state = input('是否尋找二手書(輸入y/n')
    
    if state =='y':
        
               
      
CurrentLen = WriteDataBase()
user_df = ReadDataBase()
#MonitorGoods(CurrentLen,Keyword)
#names = [product['item_basic']['name'] for product in res.json()['items']]
#print (names)