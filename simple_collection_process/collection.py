
from bs4 import BeautifulSoup #4.7.1 
from urllib.request import Request, urlopen
import csv
import argparse

'''
Usage notes
===========

Runs in python 3.6
BeautifulSoup == 4.7.1 
All others standard library tools

to run from within this repo

`python simple_collection_process/collection.py`

This will scrape 6 articles from macro section on hedgeye website.
You can add optional arguments and more pages if you'd like. Script 
uses argparse from standard library. 

Following sections can be scraped: 'macro', 'bullish', 'bearish', 'what-the-media-missed', 'cartoons', 'policy'
Max articles that can be scraped per section is 30. 

To scrape 10 articles from bearish section, run script like this:

`python simple_collection_process/collection.py --page=bearish --num_articles=10`


Images will also be downloaded to local `image` folder


'''




def collect_info(base_url, link):
    '''

    Given a url link will extract key data points from web page

    Parameters
    ==========
    base_url: str 
    link: BeautifulSoup element containing an href to search

    Returns
    =======
    dict


    '''
    
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
        row_dict['content_body_html'] = body #content_body

        #pull image
        first_image = body.find_next('img').parent['href']
        with open('images/' + title + '.png', 'wb') as f:
            f.write(urlopen(first_image).read())
            f.close()
    except AttributeError:
        row_dict['content_body_html'] = ''
    
    print('Completed info collection from {}'.format(href))
    return row_dict
    
    

def write_info(page, num_articles):
    '''
    Handles IO for scraping links

    Parameters
    ==========
    page: str, section to scrape
    num_articles: number of articles to scrape


    Returns
    =======
    None
    '''

    #metadata set up for csv file
    fieldnames = ['publish_time', 'article_title', 'writer_image_source', 'writer_name', 
                'twitter_handle', 'content_body_html']
    rows = []
    
    #beautiful soup url information to scrape
    base = 'https://app.hedgeye.com'
    section = '/insights/all?type=' + page

    #main page to find links
    base_soup = BeautifulSoup(urlopen(base + section), 'html.parser')

    #pulls links from section. 
    #collect_info function will scrape these links
    links = base_soup.find_all("div", {'class': 'thumbnail-article-quarter'})[:num_articles]

    with open('articles_metadata.csv', 'w') as articles_f:

        writer = csv.DictWriter(articles_f , fieldnames=fieldnames)
        writer.writeheader()
        
        for link in links:
            rows.append(collect_info(base, link))
        
        writer.writerows(rows)
    

if __name__ == "__main__":


    #argparsing option information
    parser = argparse.ArgumentParser(description='Tool to scrape basic data from Hedgeye site')

    parser.add_argument('--page',type=str, 
                        const='macro', 
                        nargs='?', 
                        help="select a page to scrape (default is macro)", 
                        choices=['macro', 'bullish', 'bearish', 'what-the-media-missed', 'cartoons', 'policy'])
    parser.set_defaults(page='macro')

    parser.add_argument('--num_articles', 
                        const=6, type=int, 
                        nargs='?', 
                        help='select a number of articles to scrape (default is 6)', 
                        choices=range(1,31))
    parser.set_defaults(num_articles=6)

    args = parser.parse_args()

    write_info(args.page, args.num_articles)

    