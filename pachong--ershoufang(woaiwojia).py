# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 20:53:54 2018

@author: malt927
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

url_start = 'https://hz.5i5j.com/ershoufang/'
url_list = []
url_list.append(url_start)
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
           "Cookie":"yfx_c_g_u_id_10000001=_ck18090422065113866062223058016; yfx_c_g_u_id_10000079=_ck18090517491710010317755661401; yfx_f_l_v_t_10000079=f_t_1536140956994__r_t_1536140956994__v_t_1536148724999__r_c_0; PHPSESSID=hdjib8ctl4tsgff7t45hf4lhb5; yfx_f_l_v_t_10000001=f_t_1536070011270__r_t_1536930408969__v_t_1536930408969__r_c_4; domain=hz; _Jo0OQK=27ABE8247F3787A7BAD84F321635ACE0104D03AD79F370DA3022D9E3C23B35D1C4C1AEC5A06452911DB6BBD7D2322165798D2EEE6759087C5BD51BC323791217729FFBBE0C390CBD8D41F7A141E52F240311F7A141E52F2403195090F0F6BCBDB5AF716C07F53362B87GJ1Z1Lg=="}

def getData(n):
    ##构造url_list
    for i in range(2,n+1):
        url_list.append(url_start + "n" + str(i) + '/')
        
    ##针对每一页循环
    N1 = len(url_list)
    house_lists = []
    
    for j in range(N1):
        res = requests.get(url_list[j],headers = headers)
        print (res.status_code)
        soup = BeautifulSoup(res.text,features='html.parser')
        house_html = soup.find_all("ul")[7]
        house_list = house_html.find_all("li")
        
        N2 = len(house_list)
        for i in range(N2):
            temp_list = []
            house_title = house_list[i].find("h3").text
            house_desc_temp = house_list[i].find("div",class_ = 'listX')
            house_desc_list = house_desc_temp.find_all('p')
            house_desc = house_desc_list[0].text
            house_add = house_desc_list[1].text
            house_guanzhu = house_desc_list[2].text
            house_price = house_desc_list[3].text
            house_danjia = house_desc_list[4].text
            house_tag = house_list[i].find("div",class_ = "listTag").text
            
            temp_list.append(house_title)
            temp_list.append(house_desc)
            temp_list.append(house_add)
            temp_list.append(house_guanzhu)
            temp_list.append(house_price)
            temp_list.append(house_danjia)
            temp_list.append(house_tag)
            
            house_lists.append(temp_list)
        print ("第" + str(j + 1 )+ "页已爬取完毕!")
        if (j % 100 == 0):
            print ("暂停60秒，暂停中......")
            time.sleep(60)
    data = pd.DataFrame(house_lists,columns = ["title","desc","address","guanzhudetail","price","danjia","tag"])
    data.to_excel('E:\\tianchi\\house_price\\house_hangzhou_ershoufang(woaiwojia).xlsx')
    print ("爬取完毕，已导入excel!")