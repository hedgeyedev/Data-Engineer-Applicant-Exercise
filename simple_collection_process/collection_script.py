"""
This script defines two functions.
The functions are then used to collect data and output the data in .csv form.
"""

# imports
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_links(url, num_articles=6):
    """
    Takes in a URL and desired number of links to retrieve.
    Returns a list of article links.
    """

    # create request object
    try:
        r = requests.get(url)
    except:
        print('get_links request failure.  Status code: ' + str(r.status_code))
    else:
        print('get_links request success.  Status code: ' + str(r.status_code))
    # create beautifulsoup object
    soup = BeautifulSoup(r.content, 'html.parser')

    # create empty list for links
    link_lst = []

    # get main article link
    main_link = soup.find('a', 'headline-link').get('href')
    link_lst.append(main_link)

    # get thumbnail links
    thumbnail_links = soup.find_all(
        'a', 'thumbnail-article-quarter__title-link')
    for link in thumbnail_links[:num_articles-1]:
        link_lst.append(link.get('href'))

    return link_lst


def get_article_data(url_end):
    """
    Takes in a link, appends it to a full link path.
    Retrieves data from the link path.
    Returns a dictionary of the data.
    """

    # create full link path
    url = f'https://app.hedgeye.com{url_end}'

    # create request object
    try:
        r = requests.get(url)
    except:
        print('get_links request failure.  Status code: ' + str(r.status_code))
    else:
        print('get_links request success.  Status code: ' + str(r.status_code))

    # create beautifulsoup object
    soup = BeautifulSoup(r.content, 'html.parser')

    # get datetime published
    try:
        date_time_tag = soup.find('time', {'itemprop': 'datePublished'})
        date_time = date_time_tag['datetime']
    except:
        print('article datetime error')
        date_time = ''

    # get headline
    try:
        headline = soup.find('h1', 'se-headline headline_droid').text.strip()
    except:
        print('article headline error')
        headline = ''

    # get author image href
    try:
        image_src = soup.find('div', 'headshot').find('img').get('src')
    except:
        print('author image error')
        image_src = ''

    # get author name
    try:
        full_name = soup.find('div', 'full-name').text
    except:
        print('author name error')
        full_name = ''

    # get author twitter handle
    try:
        twitter_handle = soup.find(
            'div', 'twitter-handle').find('a').get('href')
    except:
        print('twitter handle error')
        twitter_handle = ''

    # get content body html
    try:
        content_body = soup.find('div', {'itemprop': 'articleBody'})
    except:
        print('content body error')
        content_body = ''

    # create dictionary
    article_dict = {
        'published_date': date_time,
        'headline': headline,
        'img_src': image_src,
        'author_name': full_name,
        'twitter_handle': twitter_handle,
        'content_body': content_body
    }

    return article_dict


# set desired number of articles
TOTAL_ARTICLES = 6

# create list of links
ARTICLE_LINKS = get_links(
    'https://app.hedgeye.com/insights/all?type=macro', TOTAL_ARTICLES)

# create list of data dictionaires
ALL_ARTICLE_DATA = []
for lnk in ARTICLE_LINKS:
    if TOTAL_ARTICLES >= 0:
        print('Interations to go:' + str(TOTAL_ARTICLES))
        ALL_ARTICLE_DATA.append(get_article_data(lnk))
        TOTAL_ARTICLES -= 1
        time.sleep(1)
    else:
        break

# create dataframe with list of dictionaires
DF_ARTICLES = pd.DataFrame(ALL_ARTICLE_DATA)

# export dataframe to .csv file
DF_ARTICLES.to_csv('collection_data.csv', sep=',',
                   encoding='utf-8', index=None)


# # EXTRA CREDIT:

# def get_first_image(url):
#     """
#     Takes in a URL and stores a local file of the first image via the URL.
#     """
#    # create request object
#     try:
#         r = requests.get(url)
#     except:
#         print('get_links request failure.  Status code: '+ str(r.status_code))
#     else:
#         print('get_links request success.  Status code: ' + str(r.status_code))
#    # create beautifulsoup object
#     soup = BeautifulSoup(r.content, 'html.parser')
#    # get image url
#     first_img_lnk = soup.find('div', attrs={'itemprop':'articleBody'}).find('img','img-responsive').get('src')
#    # create request object
#     img_data = requests.get('https:' + first_img_lnk).content
#    # create and write image to file
#     with open('first_img.png', 'wb') as handler:
#         handler.write(img_data)

# get_first_image('https://app.hedgeye.com/insights/76737-chart-of-the-day-quad4-a-strong-dollar-story?type=macro')
