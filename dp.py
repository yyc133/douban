import requests
from lxml import etree
import re
import pymongo


# 函数功能：获取指定分类下的TOP10信息
def get_top(tu):
    data = requests.get(tu).text
    rname = re.search("type_name=(.+?)&", tu)[1]
    rid = re.search("type=(.+?)&", tu)[1]
    # print(rname, rid)
#https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20
    url = "https://movie.douban.com/j/chart/top_list?type=%s&interval_id=100:90&action=&start=0&limit=10" % rid
    data = requests.get(url, headers=header).json()
    print(data)
    #数据导入数据库MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["doubantop10"] 
    mycol = mydb["sites"]
    mycol.insert_many(data)
    


header = {
    'Cookie': '__utmc=223695111; __utmz=223695111.1571187904.9.5.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1571187903%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=858dc26640fc4e9d.1566894473.8.1571188021.1571124073.; trc_cookie_storage=taboola%2520global%253Auser-id%3D4ea59fa4-a0a2-43cf-a1a5-83751eca30fb-tuct45e61ea; __utma=223695111.1146138835.1566894471.1571124073.1571187904.9; _pk_ses.100001.4cf6=*; __utmb=223695111.0.10.1571187904; __yadk_uid=UwaYjOejdgQ6inZ7KknJCXDowV0G1jwe; acw_tc=2760820715695573523255744e3d169560489e5bab8d8b2a2b1ef09d4f1097; ck=tvj7; __utmc=30149280; __utmz=30149280.1571187886.10.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ll="118254"; push_doumail_num=0; _vwo_uuid_v2=DF1C53A0FCD5489138101210F892A63E3|e91f2af10ec0b9fe46d3a65a13c12f43; ap_v=0,6.0; bid=msLqdcqSGQs; __utma=30149280.2014424927.1566894471.1571124073.1571187886.10; __utmb=30149280.2.10.1571187886; __utmv=30149280.20286; _ga=GA1.2.2014424927.1566894471; __utmt=1; push_noty_num=0; dbcl2="202860457:yWEyZwOBnUY',
    'Host':'movie.douban.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
    }
data = requests.get("https://movie.douban.com/chart", headers=header).text
# print(re)
html = etree.HTML(data)
ht = html.xpath('//div[@class="types"]/span/a/text()')
hm = html.xpath('//div[@class="types"]/span/a/@href')
# print(ht ,hm)
hm = list(map(lambda x: "https://movie.douban.com" + x, hm))

for i in range(len(ht)):
    print(ht[i], hm[i])
    get_top(hm[i])
    

