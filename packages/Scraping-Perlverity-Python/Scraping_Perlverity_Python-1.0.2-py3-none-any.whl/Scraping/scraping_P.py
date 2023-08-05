from selenium import webdriver
from time import sleep

options = webdriver.ChromeOptions()
# 1. ヘッドレスモードでの使用
# options.add_argument('--headless')
# 2. シークレッドモードでの使用
options.add_argument('--incognito')
# 3. User-Agentの設定
options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')

# STEP1: driverを作成する
driver = webdriver.Chrome(executable_path='/Users/administrator/Google Drive/16 Python/01 Python Code/Python/91_Python_Scraping/tools/chromedriver', options=options)

# STEP2: driver.get()でサイトにアクセスする
driver.get('https://www.google.co.jp')
sleep(3)

# # STEP3: 要素を取得して、何らかの処理をかける
search_bar = driver.find_element_by_name('q')
sleep(3)

search_bar.send_keys('python')
sleep(3)

search_bar.submit()
sleep(5)

driver.quit()
