# Crawling

import csv
from bs4 import BeautifulSoup
import os
import pandas as pd
import urllib

def process(url,image_folder_name,csv_folder_name):
	r = urllib.urlopen(url).read()
	soup = BeautifulSoup(r)

	# All variables
	datetime = ""
	headline = ""
	author_exists = False
	author_name = ""
	author_image_href = ""
	author_twitter_handle = ""
	article_body = ""

	# Get datetime
	for i in soup.findAll('time'):
		if i.has_attr('datetime'): datetime = i['datetime']

	# Get headline
	headline = soup.find_all("h1", class_="se-headline")[0].get_text()

	# Get author
	for e in soup.find_all("div", class_="full-name"):
		author_exists = True
		author_name = e.get_text()


	if author_exists:
		author_image_href = soup.find_all("div", class_="headshot")[0].find('img')['src']
		author_twitter_handle = soup.find_all("div",class_="twitter-handle")[0].find('a').get_text()


	# Get article body
	article_body = "\u" + soup.find(itemprop="articleBody").get_text()

	# Save fisrt image
	path_image_folder = os.path.dirname(os.path.abspath(__file__))+"/" + image_folder_name

	# Create image folder if doesn't exist
	if not os.path.exists(path_image_folder):
		os.makedirs(path_image_folder)

	
	for image_tag in soup.find_all(itemprop="articleBody")[0].find_all('img'):
		image_href = "https:" + image_tag['src']
		destinate_path =  path_image_folder + '/' + 'test_image' + image_href[image_href.rfind('.'):]
		urllib.urlretrieve(image_href, destinate_path)
		break


	# Save other information
	path_csv_folder = os.path.dirname(os.path.abspath(__file__))+"/" + csv_folder_name

	# Create csv folder if doesn't exist
	if not os.path.exists(path_csv_folder):
		os.makedirs(path_csv_folder)

	path_csv = path_csv_folder + '/test.csv'
	lst1 = ['datetime','headline','author_exists','author_name','author_image_href','author_twitter_handle','article_body']
	lst2 = [[datetime,headline,str(author_exists),author_name,author_image_href,author_twitter_handle,article_body]]
	lst2[0] = [e.encode('utf-8') for e in lst2[0]]


	df = pd.DataFrame(lst2, columns=lst1)
	df.to_csv(path_csv)






if __name__== "__main__":
	url = 'https://app.hedgeye.com/insights/56827-investors-positioned-for-a-correction-are-positioned-for-failure'
	image_folder_name = 'images'
	csv_folder_name = 'csv'
	process(url,image_folder_name,csv_folder_name)