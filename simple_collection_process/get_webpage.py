# used Python 2.7.10 and PyCharm 2017.1.5

import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get("https://app.hedgeye.com/insights/all?type=insight")

# use BeautifulSoup to parse webpage and find content of webpage
soup = BeautifulSoup(page.content, 'html.parser')
content = soup.find(id="content")

# get all the articles
articles = content.find_all(class_="article-listing")

finMarket = articles[0]
energySect = articles[1]
tesla = articles[2]
joshCrumb = articles[3]
pensionNightmare = articles[4]
cartoon = articles[5]
genAlpha = articles[6]
earningsSeason = articles[7]
jesseFeld = articles[8]
buyingStocks = articles[9]

article_name1 = finMarket.find(class_="article-listing__heading").get_text()
article_name2 = energySect.find(class_="article-listing__heading").get_text()
article_name3 = tesla.find(class_="article-listing__heading").get_text()
article_name4 = joshCrumb.find(class_="article-listing__heading").get_text()
article_name5 = pensionNightmare.find(class_="article-listing__heading").get_text()
article_name6 = cartoon.find(class_="article-listing__heading").get_text()
article_name7 = genAlpha.find(class_="article-listing__heading").get_text()
article_name8 = earningsSeason.find(class_="article-listing__heading").get_text()
article_name9 = jesseFeld.find(class_="article-listing__heading").get_text()
article_name10 = buyingStocks.find(class_="article-listing__heading").get_text()

# request links for each article
page1 = requests.get("https://app.hedgeye.com/insights/60426-is-a-major-change-in-financial-market-sentiment-upon-us?"
                     "type=insight")
page2 = requests.get("https://app.hedgeye.com/insights/60427-stock-talk-replay-with-energy-sector-head-kevin-kaiser?"
                     "type=insight")
page3 = requests.get("https://app.hedgeye.com/insights/60469-9-reasons-to-be-bearish-on-tesla-tsla?type=insight")
page4 = requests.get("https://app.hedgeye.com/insights/60576-josh-crumb-answers-the-hedgeye-21?type=insight")
page5 = requests.get("https://app.hedgeye.com/insights/60673-the-4-trillion-nightmare-looming-over-pension-funds?"
                     "type=insight")
page6 = requests.get("https://app.hedgeye.com/insights/60738-cartoon-of-the-day-holy-cow?type=insight")
page7 = requests.get("https://app.hedgeye.com/insights/60735-mccullough-how-to-generate-alpha?type=insight")
page8 = requests.get("https://app.hedgeye.com/insights/60731-an-update-on-the-earnings-season-scorecard?type=insight")
page9 = requests.get("https://app.hedgeye.com/insights/60728-jesse-felder-answers-the-hedgeye-21?type=insight")
page10 = requests.get("https://app.hedgeye.com/insights/60723-don-t-freak-out-3-reasons-to-continue-buying-stocks-on-"
                      "pullbacks?type=insight")

article_names = [article_name1, article_name2, article_name3, article_name4, article_name5, article_name6,
                 article_name7, article_name8, article_name9, article_name10]

soup1 = BeautifulSoup(page1.content, 'html.parser')
content1 = soup1.find(id='content-container').get_text()

soup2 = BeautifulSoup(page2.content, 'html.parser')
content2 = soup2.find(id='content-container').get_text()

soup3 = BeautifulSoup(page3.content, 'html.parser')
content3 = soup3.find(id='content-container').get_text()

soup4 = BeautifulSoup(page4.content, 'html.parser')
content4 = soup4.find(id='content-container').get_text()

soup5 = BeautifulSoup(page5.content, 'html.parser')
content5 = soup5.find(id='content-container').get_text()

soup6 = BeautifulSoup(page6.content, 'html.parser')
content6 = soup6.find(id='content-container').get_text()

soup7 = BeautifulSoup(page7.content, 'html.parser')
content7 = soup7.find(id='content-container').get_text()

soup8 = BeautifulSoup(page8.content, 'html.parser')
content8 = soup8.find(id='content-container').get_text()

soup9 = BeautifulSoup(page9.content, 'html.parser')
content9 = soup9.find(id='content-container').get_text()

soup10 = BeautifulSoup(page10.content, 'html.parser')
content10 = soup10.find(id='content-container').get_text()

article_contents = [soup1, soup2, soup3, soup4, soup5, soup6, soup7, soup8, soup9, soup10]

date1 = list(content1[32:55])
datetime1 = ''.join(map(str, date1))

date2 = list(content2[32:55])
datetime2 = ''.join(map(str, date2))

date3 = list(content3[23:44])
datetime3 = ''.join(map(str, date3))

date4 = list(content4[24:42])
datetime4 = ''.join(map(str, date4))

date5 = list(content5[35:55])
datetime5 = ''.join(map(str, date5))

date6 = list(content5[34:55])
datetime6 = ''.join(map(str, date6))

date7 = list(content7[21:42])
datetime7 = ''.join(map(str, date7))

date8 = list(content8[21:42])
datetime8 = ''.join(map(str, date8))

date9 = list(content9[21:42])
datetime9 = ''.join(map(str, date9))

date10 = list(content10[21:42])
datetime10 = ''.join(map(str, date10))

datetimes = [datetime1, datetime2, datetime3, datetime4, datetime5, datetime6, datetime7, datetime8, datetime9,
             datetime10]

# get an image
img1 = soup1.find("img")
img2 = soup2.find("img")
img3 = soup3.find("img")
img4 = soup4.find("img")
img5 = soup1.find("img")
img6 = soup1.find("img")
img7 = soup1.find("img")
img8 = soup1.find("img")
img9 = soup1.find("img")
img10 = soup1.find("img")

images = [img1, img2, img3, img4, img5, img6, img7, img8, img9, img10]

df = pd.DataFrame(
    {'names': article_names,
     'datetimes': datetimes,
     'image links': images,
     #'content': article_contents
     })

print df
df.transpose()
df.to_csv('data.csv')


'''

author1 = list(content1)
author1 = [''.join(content1[0:])]
author1 = author1


# get content
soup1 = BeautifulSoup(page1.content, 'html.parser')
content1 = soup1.find(id="content").get_text()
content1 = list(content1)

# get date time
date1 = list(content1[32:53])
datetime = ''.join(map(str, date1))

# get the author
author = soup1.find_all(itemprop="articleBody")
author1 = soup1.find_all("p")
authorList = list(author1)
fin_author = authorList[32]

content1[0:] = [''.join(content1[0:])]
content1 = map(lambda x: x.strip(), content1)

data = [datetime, article_name1, fin_author, img, content1]
df = pd.DataFrame(np.array(data))
df = df.transpose()
df.columns = ['DateTime', 'ArticleTitle', 'Author', 'Image', 'Content']
print df

with open("data.csv", "w") as fn:
    writer = csv.writer(fn)
    writer.writerow(data)
fn.close()
'''''
