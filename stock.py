import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 加入繁體中文字型
fm.fontManager.addfont('TaipeiSansTCBeta-Regular.ttf')
plt.rcParams['font.family'] = ['Taipei Sans TC Beta']

# 股價波動列表
PriceChanges = []
# 時間列表
Timestamps = []

# 獲取當前時間
CurrentTime = datetime.now().strftime("%H:%M:%S")
Timestamps.append(CurrentTime)

# 使用者輸入股票代碼
StockCode = input("請輸入股票代碼:\n")
Url = 'https://tw.stock.yahoo.com/quote/' + StockCode

# 發送網絡請求
Web = requests.get(Url)
Soup = BeautifulSoup(Web.text, "html.parser")
# 獲取昨天收盤價
YesterdayClose = Soup.select('#qsp-overview-realtime-info > div:nth-child(2) > div.Fx\(n\).W\(316px\).Bxz\(bb\).Pstart\(16px\).Pt\(12px\) > div > ul > li:nth-child(7) > span.Fw\(600\).Fz\(16px\)--mobile.Fz\(14px\).D\(f\).Ai\(c\)')[0]
YesterdayClose = float(YesterdayClose.get_text())
PriceChanges.insert(0, YesterdayClose)
OpenPrice = float(YesterdayClose)
OpenPriceMax = OpenPrice + (OpenPrice * 0.1)  # 漲停價格
OpenPriceMin = OpenPrice - (OpenPrice * 0.1)  # 跌停價格

while True:
    time.sleep(5)
    CurrentTime = datetime.now().strftime("%H:%M:%S")
    Timestamps.append(CurrentTime)
    
    # 發送網絡請求
    Web = requests.get(Url)
    Soup = BeautifulSoup(Web.text, "html.parser")
              
    # 獲取目前股價和漲跌情況
    CurrentPrice = Soup.select('.Fz\(32px\)')[0]
    PriceChange = Soup.select('.Fz\(20px\)')[0]
    Title = Soup.select('.Fz\(24px\)')[0]
    
    # 將股價加入列表中
    PriceChanges.append(float(CurrentPrice.get_text()))
    
    # 繪製圖表
    plt.title(Title.get_text(), fontsize=20)
    if PriceChanges[0] < PriceChanges[-1]:
        plt.plot(Timestamps, PriceChanges, 'red', linewidth=2, markersize=6)
    elif PriceChanges[0] > PriceChanges[-1]:
        plt.plot(Timestamps, PriceChanges, 'green', linewidth=2, markersize=6)
    else:
        plt.plot(Timestamps, PriceChanges, 'black', linewidth=2, markersize=6)
        
    # 設置y軸範圍
    plt.ylim(OpenPriceMin, OpenPriceMax)
    
    # 顯示圖表
    plt.show()
