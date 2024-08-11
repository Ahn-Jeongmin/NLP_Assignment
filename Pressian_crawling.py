import requests
from bs4 import BeautifulSoup
from collections import Counter
import csv

data=[]
base_url = "https://www.pressian.com/pages/search?sort=1&search=%EC%B4%9D%EC%84%A0&startdate=2024%EB%85%84%2004%EC%9B%94%2001%EC%9D%BC&enddate=2024%EB%85%84%2004%EC%9B%94%2010%EC%9D%BC&page={}" 
html_urls = []
for page in range(1,60):
    url = base_url.format(page)
    html_urls.append(url)


# 기사 미리보기 페이지에서 추출한 기사 목록 저장을 위한 빈 배열
urls = []

for url in html_urls:

    response = requests.get(url)

    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # URL 추출
    cards = soup.select(
        'div#wrap>div#container>div.inner>div.list_search>div.section.pr10>div.arl_022>div.box>p.title>a')
    for card in cards:
        a = card['href']
        article_url="https://www.pressian.com"+a
        urls.append(article_url)

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 기사 제목 정보
    article_title = soup.select_one('div#wrap > div#container > div.inner > div.article_view > div.view_header > p.title')
    title_info = "None" if article_title is None else article_title.text.strip()

    # 기사 부제목 정보
    article_subtitle = soup.select_one('div#wrap > div#container > div.inner > div.article_view > div.view_header > p.sub_title')
    subtitle_info = "None" if article_subtitle is None else article_subtitle.text.strip()

    # 기사 날짜 정보
    article_date = soup.select_one('div#wrap > div#container > div.inner > div.article_view > div.view_header > div.box > div.byline > span.date')
    date_info = "None" if article_date is None else article_date.text.strip()

    #기자 정보
    article_journalist = soup.select_one('div#wrap > div#container > div.inner > div.article_view > div.view_header > div.box > div.byline > span.name')
    journalist_info = "None" if article_journalist is None else article_journalist.text.strip()

    #본문 정보
    article_body_element = soup.select_one('div#wrap > div#container > div.inner > div.article_view > div.section.pr10 > div.article_body')
    body_info = article_body_element.get_text(strip=True)

    article_data = {
        "title": title_info,
        "title2": subtitle_info,
        "date": date_info,
        "journalist": journalist_info,
        "article": body_info
    }
    data.append(article_data)

encoding = 'utf-8'  # 기본적으로 utf-8로 설정

# CSV 파일 생성 시 utf-8로 인코딩
try:
    with open('Pressian.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'title2', 'date', 'journalist', 'article'])
        writer.writeheader()  

        for row in data:
            writer.writerow(row)
# utf-8로 인코딩 시 에러가 발생하면 cp949로 변경하여 다시 시도
except UnicodeEncodeError:
    with open('Pressian.csv', mode='w', newline='', encoding='cp949') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'title2', 'date', 'journalist', 'article'])
        writer.writeheader()  

        for row in data:
            writer.writerow(row)


print("CSV file created.")