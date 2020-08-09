import requests, json, time, random, os
from bs4 import BeautifulSoup
import pandas as pd
import time
from sqlalchemy import create_engine

def UserAgent():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']
    UserAgent = {'User-Agent': random.choice(user_agent_list)}
    return UserAgent


def timenow():
    last_para = int(time.time() * 1000)
    now = int(time.time())
    timeArray = time.localtime(now)
    end_Time = time.strftime("%Y-%m-%d", timeArray)
    return last_para, end_Time


def macResearch_page(end_Time, last_para, UserAgent):
    # 经测试pageSize最大数值为100
    macResearchPageurl = 'http://reportapi.eastmoney.com/report/jg?pageSize=100&beginTime=2018-03-19&endTime=' + str(
        end_Time) + '&pageNo=1&fields=&qType=3&orgCode=&author=&_=' + str(last_para)
    macResearch = 'http://data.eastmoney.com/report/zw_macresearch.jshtml?encodeUrl='
    html = requests.get(macResearchPageurl, timeout=3, headers=UserAgent)
    text = html.text
    return text, macResearch


def parser_json(text, sub_url):
    djs = json.loads(text, encoding='utf-8')
    dic = {}
    for item in djs['data']:
        item_publishDate = item['publishDate'][:10].split('-')[0] + item['publishDate'][:10].split('-')[1] + \
                           item['publishDate'][:10].split('-')[2]
        pdf_title = item_publishDate + item['title']
        page_url = sub_url + item["encodeUrl"]
        dic[pdf_title] = page_url
    return dic


def save_file(dic, UserAgent, num,list):
    # num是整数并且不能超过100
    a = 0
    for key in dic.keys():
        url_r = dic[key]
        name = key
        real_html = requests.get(url_r, headers=UserAgent).text
        soup = BeautifulSoup(real_html, 'html.parser')
        file_url = soup.find_all('a', attrs={'class', 'pdf-link'})[0]['href']
        last_response = requests.get(file_url, headers=UserAgent)
        file_down = last_response.content
        file_name = name + '.' + file_url.split('.')[-1]
        content_size = int(last_response.headers['Content-Length']) / (1024 * 1024)
        inter1 = [file_name, file_url]
        list.append(inter1)
        a += 1
        if a == num:
            break
    return list
def xieru(df):
    engine = create_engine(
        'mysql+pymysql://root:lzh15679642501@jys.chinanorth.cloudapp.chinacloudapi.cn/dragon list?charset=utf8mb4')
    pd.io.sql.to_sql(df, 'yanbaofenxi', con=engine, if_exists='replace', index="False")
    print("导入成功")
def main():
    num = 50
    user_agent = UserAgent()
    last_para, end_Time = timenow()
    text, sub_url = macResearch_page(end_Time, last_para, user_agent)
    dic = parser_json(text, sub_url)
    list=[]
    list = save_file(dic, user_agent, num,list)
    df = pd.DataFrame(list,columns=["研报","链接"])
    df['研报'].astype("str")
    df['研报'] = df['研报'].map(lambda x:str(x)[: -4])
    d1 =df['研报'].str[0:8]
    df['研报'] = df['研报'].str[8:]
    df.insert(0,'时间',d1)
    df['时间'] = df['时间'].str[0:4].map(str)+"-"+df['时间'].str[4:6].map(str)+"-"+df['时间'].str[6:8].map(str)
    # d2=df['时间'].str[0:4]+'-'
    # d3=df['时间'].str[4:6]+'-'
    # d4=df['时间'].str[6:8]
    #
    xieru(df)





    # xieru(df)
main()