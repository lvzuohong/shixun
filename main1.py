#coding=gbk
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pachong_function as pf
import pandas as pd
import time

def get_dragon_list():
	html=urlopen("http://data.eastmoney.com/stock/lhb.html").read().decode('gbk')
	base="http://data.eastmoney.com"
	soup=BeautifulSoup(html,features='lxml')
	stock_urls=soup.find_all('span',{'class':"wname"})
	urls_for_base=[]
	urls_for_name=[]
	for t in stock_urls:
		urls=t.find('a')
		current=base+urls['href']
		urls_for_base.append(current)
		urls_for_name.append(urls['title'])
	return urls_for_base,urls_for_name
def compare_len(urls_for_base,urls_for_name):
	if len(urls_for_base)==len(urls_for_name):
		print("����%d��,Ԥ�ƺ�ʱ5����"%len(urls_for_base))
	else:
		print("��ȡ�Ĺ�Ʊ��ַ������������ƥ��")
		#����ȡ�������б��Ƿ�ƥ��
def get_every_stock(urls_for_base,urls_for_name):
	data=pd.DataFrame(columns=['��Ʊ����','Ӫҵ��','��/��','��λ','���'])
	for i in range(len(urls_for_base)):
		try:
			df=pf.get_detailed_info(urls_for_base[i],urls_for_name[i])
			
		except:
				print("��ȡ�����������ݳ��� "+str(urls_for_name[i])+str(urls_for_base[i]))
		else:
			data=data.append(df,ignore_index=True)
			print("�Ѿ����%d��"%(i+1))
		if i!=0 and i%30==0:
			print("�ȱ��裬��Ϣһ�£��ѱ�������")
			time.sleep(5)
			#ÿ30����Ϣʮ����,����һ��
			today=time.strftime("%Y-%m-%d")
			today="basic_data"+today+".csv"
			data.to_csv(today,encoding="utf_8_sig",)
	return data
def output_data(data):
	today=time.strftime("%Y-%m-%d")
	today="basic_data"+today+".csv"
	data.to_csv(today,encoding="utf_8_sig",)
	
def sort_the_info():
	today=time.strftime("%Y-%m-%d")
	today="basic_data"+today+".csv"
	data=pd.read_csv(today,index_col=0)
	final=pd.DataFrame(columns=['��������','�ϰ����','���һ����','����һ����','����','��Ʊ����','Ӫҵ��','��/��','��λ','���'])
	hot_money={'���ϸ�':['�й�����֤ȯ����','�й�����֤ȯ�㽭�ֹ�˾','���֤ȯ�Ϻ�½����','��̩֤ȯ�㽭�ֹ�˾','����֤ȯ���˷ֹ�˾','����֤ȯ���˽�ű�·','�й�����֤ȯ��������·','�й�����֤ȯ����������','����֤ȯ�����Ƽ�·','��̩֤ȯ�Ϻ�����·',],
			'������':['��̩���������ʺ籱·','��̩�����Ϻ���ɽ·','��֤ͨȯ�Ϻ�������·','����֤ȯ��������·','��̩֤ȯ�Ϻ�������·','��̩�����Ϻ�����·','����֤ȯ�����ļ�·','����֤ȯ�����Ӱ�·'],
			'������һ':['��̩�����Ͼ�̫ƽ��·'],			
			'���ֺ���':['����֤ȯ�����ܲ�','����֤ȯ���ں�','����֤ȯ���ں��ϴ��','�н�˾�Ƹ����˶��̱�·','�㷢֤ȯ��������·','��̩֤ȯ���ڷֹ�˾','����֤ȯ��������·','��̩֤ȯ���ڻ��ֺ���','��̩֤ȯ��������·�ٳ���������','��̩֤ȯ���ں�������',],
			'��������':['����֤ȯ�Ϻ���ƽ��·','����֤ȯ�Ϻ��챦ʯ·','����֤ȯ�ϲ�����д��','����֤ȯ�Ϻ�����·','����֤ȯ�Ϻ�ę́·','����֤ȯ�����׺�·','����֤ȯ�Ϻ��ɽ�·','����֤ȯ���������'],
			'�����̿�':['��֤ͨȯ����������','��ݸ֤ȯ�����ֹ�˾','','','',],
			'��������':['����֤ȯ�Ϻ�������·','����֤ȯ�Ϻ��ֹ�˾','�㷢֤ȯ��������·','','',],
			'��ɳ��':['����֤ȯ��������ׯ��·','����֤ȯ����Զ��·','','',],
		    '����':['����ר��']

			}
	for key,value in hot_money.items():#��������Ӫҵ��������
		hm_df,total,buy,sell,other=pf.get_hot_money(data,value)
		final=final.append({'��������':key,'�ϰ����':total,'���һ����':buy,'����һ����':sell,'����':other},ignore_index=True)
		final=final.append(hm_df,ignore_index=True)
		
	data_hx,total,buy,sell,other=pf.get_huaxin(data)
	final=final.append({'��������':"����֤ȯ",'�ϰ����':total,'���һ����':buy,'����һ����':sell,'����':other},ignore_index=True)
	final=final.append(data_hx,ignore_index=True)
	#�Ի�����������
	
	#���½������
	today=time.strftime("%Y-%m-%d")
	result=today+".xls"

	del final['index'] 
	final.to_excel(result,sheet_name="dragon list",columns=['��������','�ϰ����','���һ����','����һ����','����','��Ʊ����','Ӫҵ��','��/��','��λ','���'],encoding='utf_8_sig',index=False)

	print("��������ɣ������������������ļ�")


	print('---------------------------------------------------')

while True:
	key=input("����ѡ��\n1.һ�����������\n2.��ȡ��������������csv \n3�ӱ��ص���csv�ļ���������\n--------------------\n")
	if key == '1':
		urls_for_base,urls_for_name=get_dragon_list()
		compare_len(urls_for_base,urls_for_name)
		data=get_every_stock(urls_for_base,urls_for_name)
		output_data(data)
		sort_the_info()
		pf.change_excel()
	elif key=='2':
		urls_for_base,urls_for_name=get_dragon_list()
		compare_len(urls_for_base,urls_for_name)
		data=get_every_stock(urls_for_base,urls_for_name)
		output_data(data)
	elif key == '3':
		sort_the_info()
		pf.change_excel()
		
	else:
		exit()
