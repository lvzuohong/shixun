# coding=gbk
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pymysql
from sqlalchemy import create_engine
import pachong_function as pf
import pandas as pd
import time


def get_dragon_list():
	html = urlopen("http://data.eastmoney.com/stock/lhb.html").read().decode('gbk')
	base = "http://data.eastmoney.com"
	soup = BeautifulSoup(html, features='lxml')
	stock_urls = soup.find_all('span', {'class': "wname"})
	urls_for_base = []
	urls_for_name = []
	for t in stock_urls:
		urls = t.find('a')
		current = base + urls['href']
		urls_for_base.append(current)
		urls_for_name.append(urls['title'])
	return urls_for_base, urls_for_name


def compare_len(urls_for_base, urls_for_name):
	if len(urls_for_base) == len(urls_for_name):
		print("共计%d个,预计耗时5分钟" % len(urls_for_base))
	else:
		print("获取的股票地址和名字数量不匹配")
	# 检查获取的两个列表是否匹配


def get_every_stock(urls_for_base, urls_for_name):
	data = pd.DataFrame(columns=['股票名称', '营业部', '买or卖', '榜位', '金额/万'])
	for i in range(len(urls_for_base)):
		try:
			df = pf.get_detailed_info(urls_for_base[i], urls_for_name[i])

		except:
			print("获取个股龙虎数据出错！ " + str(urls_for_name[i]) + str(urls_for_base[i]))
		else:
			data = data.append(df, ignore_index=True)
			print("已经完成%d个" % (i + 1))
		if i != 0 and i % 30 == 0:
			print("喝杯茶，休息一下，已保留备份")
			time.sleep(5)
	return data
def sort_the_info(data):
	final = pd.DataFrame(columns=['游资名称', '上榜次数', '买榜一次数', '卖榜一次数', '其他', '股票名称', '营业部', '买or卖', '榜位', '金额/万'])
	hot_money = {'赵老哥': ['中国银河证券绍兴', '中国银河证券浙江分公司', '湘财证券上海陆家嘴', '华泰证券浙江分公司', '浙商证券绍兴分公司', '浙商证券绍兴解放北路', '中国银河证券北京阜成路',
						 '中国银河证券北京阜成门', '华鑫证券西安科技路', '银泰证券上海嘉善路', ],
				 '章盟主': ['国泰君安宁波彩虹北路', '国泰君安上海福山路', '海通证券上海建国西路', '东吴证券杭州文晖路', '中泰证券上海建国中路', '国泰君安上海江苏路', '中信证券杭州四季路',
						 '方正证券杭州延安路'],
				 '作手新一': ['国泰君安南京太平南路'],
				 '欢乐海岸': ['中信证券深圳总部', '中信证券深圳后海', '国金证券深圳海南大道', '中金公司云浮新兴东堤北路', '广发证券深圳民田路', '华泰证券深圳分公司', '中天证券深圳民田路',
						  '中泰证券深圳欢乐海岸', '华泰证券深圳益田路荣超商务中心', '华泰证券深圳海德三道', ],
				 '炒股养家': ['华鑫证券上海宛平南路', '华鑫证券上海红宝石路', '华鑫证券南昌红谷中大道', '华鑫证券上海淞滨路', '华鑫证券上海茅台路', '华鑫证券宁波沧海路', '华鑫证券上海松江路',
						  '华鑫证券西安西大街'],
				 '著名刺客': ['海通证券北京阜外大街', '东莞证券北京分公司', '', '', '', ],
				 '东北猛男': ['中信证券上海淮海中路', '中信证券上海分公司', '广发证券辽阳民主路', '', '', ],
				 '流沙河': ['招商证券北京车公庄西路', '中信证券北京远大路', '', '', ],
				 '机构': ['机构专用']
				 }
	for key, value in hot_money.items():  # 遍历游资营业部，排序
		hm_df, total, buy, sell, other = pf.get_hot_money(data, value)
		final = final.append({'游资名称': key, '上榜次数': total, '买榜一次数': buy, '卖榜一次数': sell, '其他': other}, ignore_index=True)
		final = final.append(hm_df, ignore_index=True)

	data_hx, total, buy, sell, other = pf.get_huaxin(data)
	final = final.append({'游资名称': "华鑫证券", '上榜次数': total, '买榜一次数': buy, '卖榜一次数': sell, '其他': other}, ignore_index=True)
	final = final.append(data_hx, ignore_index=True)
	return final
def shujuku():
	conn = pymysql.connect(
		host="jys.chinanorth.cloudapp.chinacloudapi.cn",
		port=3306,
		user="root",
		password="lzh15679642501",
		db="dragon list",
		charset="utf8"
	)
	cls = conn.cursor()


def xieru(final):
	final = final.applymap(lambda x: x if str(x) != 'nan' else None)
	engine = create_engine('mysql+pymysql://root:lzh15679642501@jys.chinanorth.cloudapp.chinacloudapi.cn/dragon list?charset=utf8mb4')
	pd.io.sql.to_sql(final, 'erp_source', con=engine, if_exists='replace', index="False")
	print("数据导入成功")

def paquzhixing():
	urls_for_base, urls_for_name = get_dragon_list()
	compare_len(urls_for_base, urls_for_name)
	data = get_every_stock(urls_for_base, urls_for_name)
	final = sort_the_info(data)
	xieru(final)

paquzhixing()
