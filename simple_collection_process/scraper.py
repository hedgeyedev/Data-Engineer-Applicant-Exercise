import requests, csv, shutil,sys
from bs4 import BeautifulSoup

print('This program scrapes to "data.csv" in your currenty directory')
print('the first 6 images from each article are also included as "img(n)"')
print('Scraping...')

#Cleans up excess whitespace that makes the data hard to view in Excel (Numbers automatically resizes cells to make the data easier to view)
def clean(string):
    return ' '.join(string.split())

try:
    request = requests.get('https://app.hedgeye.com/insights/all?type=insight')

except requests.exceptions.RequestException as e:
    print('It looks like you have a connection problem')
    print(e)
    sys.exit(1)

soup = BeautifulSoup(request.text, 'html.parser')
notes = soup.find_all('div',class_='note')

articles = []

with open('data.csv', 'w') as csvfile:
    for note in notes:
        csvwriter = csv.writer(csvfile, dialect='excel')
        csvwriter.writerow(['Article Title',clean(note.find('h1',class_='se-headline headline_droid').getText())])
        csvwriter.writerow(['Datetime Published',note.find('time').get('datetime')]) #picked this over the span you see on the page, because it has seconds in addition to hours and minutes
        csvwriter.writerow(['Author Name',clean(note.find('div',class_ = 'full-name').getText()) if note.find('div',class_ = 'full-name') != None else 'None'])
        csvwriter.writerow(['Twitter Handle',clean(note.find('div',class_ = 'twitter-handle').getText()) if note.find('div',class_ = 'twitter-handle') != None else 'None'])
        csvwriter.writerow(['Author Picture Link',note.find('div',class_ = 'headshot').next_element.get('src') if note.find('div',class_ = 'headshot') != None else 'None'])
        article_html = note.find('div',itemprop = 'articleBody')
        csvwriter.writerow(['Note Body HTML',article_html])
        articles.append(article_html)

img_number = 1

for article in articles:
    img = requests.get('http:'+article.find('img').get('src'),stream=True)
    with open('img'+str(img_number), 'wb') as output:
        shutil.copyfileobj(img.raw, output)
    img_number += 1

print('Done!')