
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import csv



def collect_info(base_url, link):
    
    row_dict = {}
    href = link.find('a')['href']
    #print(href)
    soup = BeautifulSoup(urlopen(base_url + href), 'html.parser')    

    try:
        row_dict['publish_time'] = soup.find("div", {"class": "tags"}).time.text.strip('\n')#publish time
    except AttributeError:
        row_dict['publish_time'] = ''

    try:
        title = soup.find("div", {"class": "headline-link"}).text.strip('\n')
        row_dict['article_title'] = title #article_title,
    except AttributeError:
        row_dict['article_title'] = ''

    try:
        source = soup.find("div", {"class": "headshot"}).find('img')['src']
        row_dict['writer_image_source'] = source # headshot_img_src
    except:
        row_dict['writer_image_source'] = ''

    try:
        row_dict['writer_name'] = soup.find("div", {"class": "full-name"}).text #writer_name
    except AttributeError:
        row_dict['writer_name'] = ''

    try:
        row_dict['twitter_handle'] = soup.find("div", {"class": "twitter-handle"}).text.strip('\n'), #twitter_handle
    except AttributeError:
        row_dict['twitter_handle'] = ''

    try:
        body = soup.find("div", {"itemprop": "articleBody"})
        row_dict['content_body_html'] = body #twitter_handle
        first_image = body.find_next('img').parent['href']
        with open('images/' + title + '.png', 'wb') as f:
            f.write(urlopen(first_image).read())
            f.close()
    except AttributeError:
        row_dict['content_body_html'] = ''
    
    print('Completed info collection from {}'.format(href))
    return row_dict
    
    
    

if __name__ == "__main__":
    
    fieldnames = ['publish_time', 'article_title', 'writer_image_source', 'writer_name', 
                'twitter_handle', 'content_body_html']
    rows = []
    
    base = 'https://app.hedgeye.com'
    macro = '/insights/all?type=macro'

    base_soup = BeautifulSoup(urlopen(base + macro), 'html.parser')
    links = base_soup.find_all("div", {'class': 'thumbnail-article-quarter'})[:6]
    
    with open('articles_metadata.csv', 'w') as articles_f:

        writer = csv.DictWriter(articles_f , fieldnames=fieldnames)
        writer.writeheader()
        
        for link in links:
            rows.append(collect_info(base, link))
        
        
        
        writer.writerows(rows)