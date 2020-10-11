from selenium import webdriver
import time


driver = webdriver.Chrome()
driver.get('https://www.processon.com/login')
time.sleep(1)

# 填写账号
driver.find_element_by_id('login_email').send_keys('diligent2333@163.com')
driver.find_element_by_id('login_password').send_keys('123abc')
time.sleep(2)

# 点击登陆
driver.find_element_by_id('signin_btn').click()

time.sleep(3)
driver.close()
