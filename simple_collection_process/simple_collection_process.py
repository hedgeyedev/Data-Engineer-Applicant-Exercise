import requests
from bs4 import BeautifulSoup
import urllib

# make sure install bs4 and requests
authorInfo=0
# function toe extract contents from home page.
def extract_main_page(page):
    articles_list=[]
    response = requests.get(page)
    soup = BeautifulSoup(response.content, 'html.parser')
    web_pages = soup.find('div', attrs={'class':'col-md-8', 'id':'recent'})
    row=web_pages.find('div',attrs={'class':'row'})
    count=0
    for eachdiv in row.findAll('div',recursive=False):
        if count > 5:
            break
        else:
            if (str(eachdiv.get("class")[0]) == "col-md-12"):
                article=eachdiv.find('div',attrs={'class':'large-article'})
                link =article.find('a')
                articles_list.append(str(page) + str(link.attrs['href']))
            elif (str(eachdiv.get("class")[0]) == "col-sm-12"):
                article=eachdiv.find('div',attrs={'class':'med-article med-article_home'})
                row=article.find('div',attrs={'class':'row'})
                tag=row.find('div',attrs={'class':'col-sm-6'})
                link=tag.find('a')
                articles_list.append(str(page) + str(link.attrs['href']))
            count+=1
    for eacharticle in articles_list:
        robust_requests(eacharticle)

def encodestring(string):
    return ''.join(string).encode('utf-8')

# function for making web requests
def robust_requests(page):
    page = requests.get(page)
    extract_html(page)

# function to extract html contents from webpage using beautifulsoup lib
def extract_html(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    web_contents=soup.find_all('div', class_='note')
    write_tocsv(web_contents)

# function to write scrapped contents to csv file
def write_tocsv(web_contents):
    global authorInfo
    import csv
    articles=[]
    with open('scrapped_contents.csv', 'a') as csvfile:
        for content in web_contents:
            csvwriter = csv.writer(csvfile, dialect='excel')
            body=content.find('div', attrs={'class': 'body'})
            headLine=body.find('h1').getText()
            csvwriter.writerow(['Article Title',encodestring(headLine)])
            csvwriter.writerow(['Datetime Published',body.find('time').get('datetime')])
            if authorInfo==0 and body.find('div',attrs={'class':'row bylines'}):
                rowbylines=body.find('div',attrs={'class':'row bylines'})
                byline=rowbylines.find('div',attrs={'class':'byline pull-left clearfix'})
                if byline.find('div',attrs={'class':'headshot'}):
                   headshot=byline.find('div',attrs={'class':'headshot'})
                   image=headshot.find('image')
                   imageUrl=str(image.attrs['src'])
                   csvwriter.writerow(['Image URL',imageUrl])
                   fullname=byline.find('div',attrs={'class':'full-name'})
                   csvwriter.writerow(['Author Name',fullname])
                   authorInfo=1
                   if byline.find('div',attrs={'class':'twitter-handle'}):
                      twitter_handle=byline.find('div',attrs={'class':'twitter-handle'})
                      link=twitter_handle.find('a').getText()
                      csvwriter.writerow(['Twitter Handle',link])
                   else:
                      csvwriter.writerow(['Twitter Handle',''])
            if body.find('div',attrs={'class':'premium-insights-header'}):
               articlecontent=content.find('p').getText()
               print articlecontent
               csvwriter.writerow(['Body',encodestring(articlecontent)])
            else:
                article_html = content.find('div',itemprop = 'articleBody')
                csvwriter.writerow(['Body',article_html])

# main driver
if __name__ == '__main__':
    f = open("scrapped_contents.csv",'w')
    extract_main_page("https://app.hedgeye.com")
    print('completed')
