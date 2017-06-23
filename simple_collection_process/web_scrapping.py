NEWS_2_READ = 6


def write_2_csv(my_dict, path='./output/articles_details.csv'):
    import csv
    import os

    try:
        if os.path.exists(path):
            with open(path, 'a', encoding='utf-8', newline='') as csv_file:
                fieldnames = ['Datetime', 'Headline', 'Author Name', 'Author Image', 'Author Twitter', 'Content']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writerow({
                    'Datetime': my_dict['datetime'],
                    'Headline': my_dict['headline'],
                    'Author Name': my_dict['author_name'],
                    'Author Image': my_dict['author_image'],
                    'Author Twitter': my_dict['author_twitter'],
                    'Content': my_dict['content']
                })
                csv_file.close()
        else:
            with open(path, 'w', encoding='utf-8', newline='') as csv_file:
                fieldnames = ['Datetime', 'Headline', 'Author Name', 'Author Image', 'Author Twitter', 'Content']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({
                    'Datetime': my_dict['datetime'],
                    'Headline': my_dict['headline'],
                    'Author Name': my_dict['author_name'],
                    'Author Image': my_dict['author_image'],
                    'Author Twitter': my_dict['author_twitter'],
                    'Content': my_dict['content']
                })
                csv_file.close()
    except:
        raise RuntimeError('Error when saving to CSV file.')
    return


def save_img_2_disk(soup):
    from urllib import request
    import os

    try:
        for a in soup.find('div', itemprop='articleBody').find_all('a', href=True):
            ref = a['href']
            if '.jpg' in ref or '.png' in ref or '.gif' in ref:
                request.urlretrieve(ref, './output/' + os.path.basename(ref))
                break
            del ref
    except:
        raise RuntimeError('Error when saving image to disk.')
    return


def get_data(soup, info):

    try:
        info['datetime'] = (soup.find("time", itemprop='datePublished').get_text()).replace('\n', '')
        info['headline'] = soup.find('title').get_text()
        info['content'] = str.encode(str(soup.find('body')).replace(' ', ''))

        if soup.find('div', class_='headshot') is None:
            info['author_image'] = 'N/A'
            info['author_name'] = 'HEDGEYE Guest'
            info['author_twitter'] = 'N/A'
        else:
            info['author_image'] = soup.find('div', class_='byline').find('img')['src']
            info['author_name'] = soup.find('div', class_='full-name').get_text()
            info['author_twitter'] = soup.find('div', class_='twitter-handle').find('a').get_text()

        return info
    except:
        raise RuntimeError('Error getting data.')


if __name__ == '__main__':
    import requests
    from bs4 import BeautifulSoup

    page = requests.get('https://app.hedgeye.com/insights/all?type=insight')

    if page.status_code != 200:
        print('Something is wrong with the website, HTML error: {}'.format(page.status_code))
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        articles_href = soup.find_all('a', class_='thumbnail-article__title-link', href=True)
        hrefs = [article['href'] for article in articles_href[:NEWS_2_READ]]
        del articles_href

        for ref in hrefs:
            url = 'https://app.hedgeye.com' + ref
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            article_url = requests.get(url, headers)

            if article_url.status_code != 200:
                print('Something is wrong with the Article website, HTML error: {}'.format(article_url.status_code))
            else:
                article_soup = BeautifulSoup(article_url.content, 'html.parser')

                info = dict()
                info = get_data(article_soup, info)
                write_2_csv(info)
                del info
                save_img_2_disk(article_soup)
