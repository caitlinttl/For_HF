# -----網址解析
from urllib.parse import urlparse
url = 'https://www.ncbi.nlm.nih.gov/pubmed/?term=tDCS'
o = urlparse(url)
print(o)


# -----網頁資料擷取
import requests

url = 'https://web.ym.edu.tw/bin/home.php'
html = requests.get(url)
html.encoding="utf-8"

htmllist = html.text.splitlines()
n = 0
for row in htmllist:
    if '企鵝' in row: n += 1
    # print(row)
print(f"出現{n}次企鵝")


# -----BeautifulSoup 網頁解析
from bs4 import BeautifulSoup
import requests

url = 'http://www.e-happy.com.tw'
html = requests.get(url)
html.encoding="utf-8"

sp=BeautifulSoup(html.text,"html.parser")
links=sp.find_all("a") # 讀取 <a>
for link in links:
    href=link.get("href") # 讀取 href 屬性內容
    # 判斷內容是否為非 None，並且開頭文字是 http://
    if  href != None and href.startswith("http://"): 
        print(href)


# -----下載指定網頁的圖片
import requests,os
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = 'https://www.dreamstime.com/free-images_pg1'

html = requests.get(url)
html.encoding="utf-8"

sp = BeautifulSoup(html.text, 'html.parser')

# 建立 images 目錄儲存圖片
images_dir="images/"
if not os.path.exists(images_dir):
    os.mkdir(images_dir)
    
# 取得所有 <a> 和 <img> 標籤
all_links=sp.find_all(['a','img']) 
for link in all_links:
    # 讀取 src 和　href 屬性內容
    src=link.get('src')
    href = link.get('href')
    attrs=[src,href]
    for attr in attrs:
        # 讀取　.jpg 和　.png 檔
        if attr != None and ('.jpg' in attr or '.png' in attr):
            # 設定圖檔完整路徑
            full_path = attr            
            filename = full_path.split('/')[-1]  # 取得圖檔名
            print(full_path)
            # 儲存圖片
            try:
                image = urlopen(full_path)
                f = open(os.path.join(images_dir,filename),'wb')
                f.write(image.read())
                f.close()
            except:
                print("{} 無法讀取!".format(filename))


