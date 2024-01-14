# %%
import os
import re
from jsonpath import jsonpath
import requests
import pandas as pd
import datetime

# %%
def trans_time(v_str):
    """转换GMT时间为标准格式"""
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
    ret_time = timeArray.strftime("%Y-%m-%d %H:%M:%S")
    return ret_time

# %%
def get_weibo_list(v_keyword,v_max_page):
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    }

    for page in range(1,v_max_page +1):
        print('===开始爬取第{}页微博==='.format(page))
        #请求地址
        # 请求地址
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%23iphone%23&page_type=searchall'
        # 请求参数
        params = {
        "containerid": "100103type=1&q=#iphone#",
        "page_type": "searchall",
        "page": page
        }
        # 发送请求
        r = requests.get(url, headers=headers, params=params)
        print(r.status_code)
        #pprint(r.json())
        #解析json数据
        cards = r.json()["data"]["cards"]
        #微博内容
        text_list=jsonpath(cards, '$..mblog.text')
        #微博内容-正则表达式数据清洗
        dr = re.compile(r'<[^>]+>', re.S)
        text2_list =[]
        #print('text_list is:')
        #print(text_list)
        if not text_list:
            continue
        if type(text_list)==list and len(text_list)>0:
            for text in text_list:
                text2=dr.sub('', text)
                print(text2)
                text2_list.append(text2)
        #微博创建时间
        time_list = jsonpath(cards, '$..mblog.created_at')
        time_list=[trans_time(v_str=i) for i in time_list]
        #微博作者
        author_list = jsonpath(cards, '$..mblog.user.screen_name')
        #微博id
        id_list =jsonpath(cards, '$..mblog.id')
        #微博bid
        bid_list = jsonpath(cards, '$..mblog.bid')
        # 转发数
        reposts_count_list = jsonpath(cards, '$..mblog.reposts_count')
        # 评论数
        comments_count_list = jsonpath(cards, '$..mblog.comments_count')
        # 点赞数
        attitudes_count_list = jsonpath(cards, '$..mblog.attitudes_count')

        df = pd.DataFrame(
        {
        '页码': [page] * len(id_list),
        '微博id': id_list,
        '微博bid': bid_list,
        '微博作者': author_list,
        '发布时间': time_list,
        '微博内容': text2_list,
        '转发数': reposts_count_list,
        '评论数': comments_count_list,
        '点赞数': attitudes_count_list,
        }
        )

        if os.path.exists(v_weibo_file):  # 如果文件存在，不再设置表头
            header = None
        else:  # 否则，设置csv文件表头
            header = ['页码','微博id','微博bid','微博作者','发布时间','微博内容','转发数','评论数','点赞数']
        # 保存csv文件
        df.to_csv(v_weibo_file, mode='a+', index=False, header=header, encoding='utf_8_sig')
        print('结果保存成功:{}'.format(v_weibo_file))
        print(df)

if __name__ == '__main__':
    max_search_page = 100
    search_keyword = '#iphone#'
    v_weibo_file = '微博清单.csv'
    # 如果结果文件存在，先删除
    if os.path.exists(v_weibo_file):
        os.remove(v_weibo_file)
        print('csv文件已存在,先删除:{}'.format(v_weibo_file))
    get_weibo_list(v_keyword=search_keyword, v_max_page=max_search_page)
    df =pd.read_csv(v_weibo_file)
    # 删除重复数据
    df.drop_duplicates(subset=['微博bid'], inplace=True, keep='first')
    df.to_csv(v_weibo_file, index=False, encoding='utf_8_sig')
    print('数据清洗完成')
    


        



