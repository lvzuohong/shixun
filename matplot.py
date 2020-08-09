from sqlalchemy import create_engine
import pandas as pd
import pymysql
import sqlalchemy
import matplotlib.pyplot as plt
from datetime import datetime,date,timedelta
import matplotlib.ticker as ticker

engine = create_engine('mysql+pymysql://root:lzh15679642501@jys.chinanorth.cloudapp.chinacloudapi.cn/dragon list?charset=utf8mb4')
sql_cmd = "select * from today_zhangdie"
df =pd.read_sql(sql=sql_cmd, con=engine)
d1 =df.loc[0]
d2 = df.loc[11]
d_1 =d1[2:12]
d_2 =d2[2:12]
d_1 =d_1.astype("float")
d_2 =d_2.astype("float")

def get_riqi():
    count=8
    i=0
    today = date.today()
    riqi_list =[]
    riqi_list.append(str(today))
    while(i<=count):
        i+=1
        riqi_list.append(str((today+timedelta(days=-i))))
    return riqi_list

riqi_list = get_riqi()
rili =[]
for riqi in riqi_list:
    rili.append(riqi[5:])
#绘制图形
plt.figure(figsize=(10,5))
# plt.style.use('dark_background')
plt.title('涨停和开板数的走势图',color='black')
plt.rcParams['font.sans-serif']=['SimHei']
plt.xlabel('时间')
plt.ylabel('数量')
plt.plot(rili[::-1],d_1,label='涨停',linewidth=2,color='red',marker='o',markerfacecolor='white',markersize=4)
plt.plot(rili[::-1],d_2,label='开板数',linewidth=2,color ='green',marker='o',markerfacecolor='white',markersize=4)
plt.grid(color='DimGray')
plt.legend(['涨停','开板数'])
# plt.savefig(r'E:\python1\app\static\test.png',bbox_inches = 'tight')
plt.savefig(r'E:\python1\app\static\test.png',bbox_inches = 'tight',transparent = True)

