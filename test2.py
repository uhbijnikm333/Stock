import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm

fm.fontManager.addfont('TaipeiSansTCBeta-Regular.ttf')
mpl.rc('font', family='Taipei Sans TC Beta')
#使用繁體中文套件

list= [] #股價的波動list
currentDateAndTime =[]#時間軸list
time_now = datetime.now().strftime("%H:%M:%S")
currentDateAndTime.append(time_now)
code = input("請輸入股票代碼:\n")
url = 'https://tw.stock.yahoo.com/quote/2330'
web = requests.get(url)                          # 取得網頁內容
soup = BeautifulSoup(web.text, "html.parser")
Open = soup.select('#qsp-overview-realtime-info > div:nth-child(2) > div.Fx\(n\).W\(316px\).Bxz\(bb\).Pstart\(16px\).Pt\(12px\) > div > ul > li:nth-child(7) > span.Fw\(600\).Fz\(16px\)--mobile.Fz\(14px\).D\(f\).Ai\(c\)')[0]
Open = float(Open.get_text())#找到昨天收盤價格
list.insert(0, Open)
OpenPrice = float(Open)
OpenPriceMax = (OpenPrice+(OpenPrice*0.1))#漲停價格
OpenPriceMin = (OpenPrice-(OpenPrice*0.1))#跌停價格

while True:
    time.sleep(5)
    time_now = datetime.now().strftime("%H:%M:%S")
    currentDateAndTime.append(time_now)
    
    web = requests.get(url)                          # 取得網頁內容
    soup = BeautifulSoup(web.text, "html.parser")    # 轉換內容
              
    a = soup.select('.Fz\(32px\)')[0]     # 找到目前股價的價格的select class
    b = soup.select('.Fz\(20px\)')[0]     # 找到目前股價的漲跌的select class
    s = '' 
    title = soup.select('.Fz\(24px\)')[0]
    
    list.append(float(a.get_text()))
    plt.title(title.get_text(), fontsize=20)
    if list[0] <list[-1]:
        s = '+'
        plt.plot(currentDateAndTime, list, 'red', linewidth=2, markersize=6)
    elif list[0] >list[-1]:
        s = '-'
        plt.plot(currentDateAndTime, list, 'green', linewidth=2, markersize=6)
    else :
        plt.plot(currentDateAndTime, list, 'black', linewidth=2, markersize=6)
        s = ' '
    print(f'{title.get_text()} : {a.get_text()} ( {s}{b.get_text()} )')   # 印出結果    
    plt.ylim(OpenPriceMin, OpenPriceMax)
    #plt.xlim(start_time,end_time)
    plt.show()