import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import os

cookie = '__mta=209498669.1600777449132.1601110785065.1601114444345.22; uuid_n_v=v1; uuid=81860D10FCCE11EA8ECD3DB0936FC6C2155EA4AF29354BB0BC6C5DE7D6E449AE; _lxsdk_cuid=174b5c5601cc8-0deff943135f12-5313f6f-13c680-174b5c5601cc8; _lxsdk=81860D10FCCE11EA8ECD3DB0936FC6C2155EA4AF29354BB0BC6C5DE7D6E449AE; mojo-uuid=5b689612d14851df2d978834ba8363b4; _csrf=05b9b07c3a3938ff964737ad56d5bd6e975e49163080b8c4efd94be3dc069875; mojo-session-id={"id":"73109e1ca5bc4fb323a167c72c2de2a7","time":1601114444101}; mojo-trace-id=2; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1600777445,1601022326,1601022812,1601114699; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1601114699; __mta=209498669.1600777449132.1601114444345.1601114699401.23; _lxsdk_s=174c9db9135-daa-0f0-264%7C%7C6'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
headers = {'User-Agent': user_agent, 'Cookie': user_agent}


# 从子链接中提取数据
def get_data(url):
    response = requests.get(url=url, headers=headers)
    soup = bs(response.text, 'html.parser')
    tag = soup.find('div', attrs={'class': 'movie-brief-container'})
    file_name = tag.h1.text
    file_types = '，'.join(x.text.strip() for x in tag.ul.li.find_all('a'))  # ul 下面的第一个 li 标签，下面再是所有 a 标签
    # file_types = ','.join(x.text.strip() for x in tag.ul.find('li').find_all('a'))  # 等同
    file_date = tag.ul.find_all('li')[-1].text
    return file_name, file_types, file_date


response = requests.get('https://maoyan.com/films?showType=1', headers=headers)
soup = bs(response.text, 'html.parser')

# # 得到数据，一行一行添加
for tag in soup.find_all('div', attrs={'class': 'movie-item film-channel'}, limit=10):
    url = 'https://maoyan.com' + tag.a.get('href')
    print(url)
    # 数据形状：(3,) --> (1,3)
    df = pd.DataFrame(np.array(get_data(url)).reshape(1, 3))
    print(df)
    # 第一次存数据将 header 也写入文件
    if not os.path.isfile('movie.csv'):
        df.to_csv('movie.csv', mode='a', index=False, header=['name', 'types', 'date'], encoding='utf-8')
    else:
        df.to_csv('movie.csv', mode='a', index=False, header=False, encoding='utf-8')

# names, types, dates = [], [], []
# for tag in soup.find_all('div', attrs={'class': 'movie-item film-channel'}, limit=10):
#     url = 'https://maoyan.com' + tag.a.get('href')
#     file_name, file_types, file_date = get_data(url)
#     names.append(file_name)
#     types.append(file_types)
#     dates.append(file_date)
#
# df = pd.DataFrame([names, types, dates], columns=['name', 'type', 'date'])
# print(df)