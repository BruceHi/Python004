import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
headers = {
    'User-agent': ua.random,
    'Referer': 'https://www.processon.com/login?f=index'
}

# 开启会话
s = requests.Session()
login_url = 'https://www.processon.com/login'
foam_data = {
    'login_email': 'diligent2333@163.com',
    'login_password': '123abc',
}
response = s.post(login_url, data=foam_data, headers=headers)

print(response.status_code)
with open('content.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
