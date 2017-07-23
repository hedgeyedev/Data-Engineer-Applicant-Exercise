import requests
from bs4 import BeautifulSoup

# get the webpage and check the status of it
page = requests.get("https://app.hedgeye.com/insights/all?type=insight")
print page.status_code

# use BeautifulSoup to parse webpage and find content of webpage
soup = BeautifulSoup(page.content, 'html.parser')
content = soup.find(id="content")
# print content

# get all the articles
articles = content.find_all(class_="article-listing")
# print articles

# parse the first article
article1 = articles[0]
name1 = article1.find(class_="article-listing__heading").get_text()

#request the link for first article
page1 = requests.get("https://app.hedgeye.com/insights/60426-is-a-major-change-in-financial-market-sentiment-upon-us?"
                     "type=insight")
# get content 
soup1 = BeautifulSoup(page1.content, 'html.parser')
content1 = soup1.find(id="content").get_text()

#get date time
date1 = list(content1[32:50])
datetime = ''.join(map(str, date1))

#get the author
author = soup1.find_all(itemprop="articleBody")
author1 = soup1.find_all("p")
authorList = list(author1)
fin_author = authorList[32]

#get an image
img = soup1.find("img")

print datetime
print name1
print fin_author
print content1
print img
