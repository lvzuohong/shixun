import pandas as pd
import xlwt
import time
import requests
from bs4 import BeautifulSoup
import pymysql
from sqlalchemy import create_engine

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}#爬虫[Requests设置请求头Headers],伪造浏览器
# 核心爬取代码
url= 'http://wuylh.com/'
params = {"show_ram":1}
response = requests.get(url,params=params, headers=headers)#访问url
response.encoding='UTF-8'
listData=[]#定义数组
soup = BeautifulSoup(response.text, 'html.parser')#获取网页源代码
tr = soup.find('table',class_='rt cf two').find_all('tr')#.find定位到所需数据位置  .find_all查找所有的tr（表格）
# 去除标签栏
th = soup.find('table',class_='rt cf two').find_all('th')
for i in range(len(th)):
    time1 =th[i].get_text()
    listData.append(time1)
listData.remove('时间')
d1=pd.DataFrame(listData)
d1=d1.T
listData.clear()
print(d1)
for j in tr[1:]:        #tr2[1:]遍历第1列到最后一列，表头为第0列
    td = j.find_all('td')#td表格
    zht = td[0].get_text().strip()           #遍历涨停
    yz = td[1].get_text().strip()  #遍历一字
    erl = td[2].get_text().strip()
    sl = td[3].get_text().strip()
    sli= td[4].get_text()
    wl = td[5].get_text()
    jz=td[6].get_text()
    sz=td[7].get_text()
    wq=td[8].get_text()
    wh=td[9].get_text()
    wp=td[10].get_text()

    listData.append([zht,yz,erl,sl,sli,wl,jz,sz,wq,wh,wp])
print (listData)#打印
dataframe=pd.DataFrame(listData)
print(dataframe)
# dataframe.to_excel('D:\\2020暑期实习\\文档列表\\listData.xls')

def daorushuju(dataframe):
    engine = create_engine('mysql+pymysql://root:lzh15679642501@jys.chinanorth.cloudapp.chinacloudapi.cn/dragon list?charset=utf8mb4')
    pd.io.sql.to_sql(dataframe, 'today_zhangdie', con=engine, if_exists='replace', index="False")
    print("导入成功")
def  daoruriqi(d1):
    engine = create_engine('mysql+pymysql://root:lzh15679642501@jys.chinanorth.cloudapp.chinacloudapi.cn/dragon list?charset=utf8mb4')
    pd.io.sql.to_sql(d1, 'riqi', con=engine, if_exists='replace', index="False")
    print("导入成功")
daorushuju(dataframe)
daoruriqi(d1)


