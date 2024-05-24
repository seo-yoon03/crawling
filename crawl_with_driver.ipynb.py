from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
import os

# ChromeDriver 경로 설정
chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# 구글 이미지 검색 URL로 이동
query = "beautiful roses"
url = f"https://www.google.com/search?q={query}&tbm=isch"
driver.get(url)

# 저장 디렉토리 설정
save_dir = "downloaded_images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 스크롤 다운 반복
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# BeautifulSoup로 HTML 파싱
soup = BeautifulSoup(driver.page_source, 'html.parser')
img_tags = soup.find_all('img')

# 이미지 다운로드
for idx, img_tag in enumerate(img_tags):
    img_url = img_tag.get('src')
    
    # 데이터 URL 건너뛰기
    if img_url and img_url.startswith('data:image/'):
        continue
    
    try:
        img_data = requests.get(img_url).content
        filename = f"image_{idx}.jpg"
        filepath = os.path.join(save_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(img_data)
        print(f"{filename} 다운로드 완료")
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

driver.quit()