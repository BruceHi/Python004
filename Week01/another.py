import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

cookie = '__mta=209498669.1600777449132.1601110785065.1601114444345.22; uuid_n_v=v1; uuid=81860D10FCCE11EA8ECD3DB0936FC6C2155EA4AF29354BB0BC6C5DE7D6E449AE; _lxsdk_cuid=174b5c5601cc8-0deff943135f12-5313f6f-13c680-174b5c5601cc8; _lxsdk=81860D10FCCE11EA8ECD3DB0936FC6C2155EA4AF29354BB0BC6C5DE7D6E449AE; mojo-uuid=5b689612d14851df2d978834ba8363b4; _csrf=05b9b07c3a3938ff964737ad56d5bd6e975e49163080b8c4efd94be3dc069875; mojo-session-id={"id":"73109e1ca5bc4fb323a167c72c2de2a7","time":1601114444101}; mojo-trace-id=2; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1600777445,1601022326,1601022812,1601114699; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1601114699; __mta=209498669.1600777449132.1601114444345.1601114699401.23; _lxsdk_s=174c9db9135-daa-0f0-264%7C%7C6'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
headers = {'User-Agent': user_agent, 'Cookie': user_agent}

response = requests.get('https://maoyan.com/films?showType=1', headers=headers)
soup = bs(response.text, 'html.parser')

names, types, dates = [], [], []
# 得到数据，整体添加
for tag in soup.find_all('div', attrs={'class': 'movie-hover-info'}, limit=10):
    info = tag.find_all('div')
    file_name = info[0].span.text
    file_types = info[1].contents[-1].strip()
    file_date = info[-1].contents[-1].strip()
    names.append(file_name)
    types.append(file_types)
    dates.append(file_date)

df = pd.DataFrame({'电影名称': names, '类型': types, '上映日期': dates})
df.to_csv('movies_another.csv', index=False, encoding='utf-8')
