# Jeff Falberg
# simple collection process exercise

import urllib.request as urr
import urllib.error
from urllib.parse import quote
from urllib.error import HTTPError
import sys
import re
import os

# Print output to csv file
sys.argv = ["simple_collection_process.py", "output.csv"]
output_file = sys.argv[1]
output_csv = open(output_file, "w", encoding='utf-8')

# open home page of articles
url = "https://app.hedgeye.com/insights/all?type=insight"
page = urr.urlopen(url)
if page.getcode() == 200 :
	sourcepage = page.read()
	source = sourcepage.decode("utf-8")
	# compile array of the five most recent article URLs in addition to the newest one
	articles = []
	articles.append(url)
	for i in range(1, 6) :
		regexArticle = re.compile("<div class='thumbnail-article'>.*?<a href='(.*?)'>", re.DOTALL)
		article = re.findall(regexArticle, source)[i]
		article = "https://app.hedgeye.com"+article
		articles.append(article)
	# confirm article links
	print(articles)
	# open each article URL in array to collect data
	for i in range(0, len(articles)): 
		url = articles[i]
		page = urr.urlopen(url)
		if page.getcode() == 200 :
			sourcepage = page.read()
			source = sourcepage.decode("utf-8")
			print("Processing: "+url)
			# fetch datetime
			regexDate = re.compile(r"time datetime.*?<span>(\d.*?)</span>", re.DOTALL)
			datetime = re.findall(regexDate, source)[0]
			# fetch headline
			regexHeadline = re.compile(r"<h1 class='se-headline headline_droid' itemprop='name'>(.*?)</h1>", re.DOTALL)
			headline = re.findall(regexHeadline, source)[0]
			headline = re.sub('\n','',headline)
			# fetch author image
			try:
				regexHeadshot = re.compile(r"headshot.*?src=\"(.*?)\" /", re.DOTALL)
				headshot = re.findall(regexHeadshot, source)[0]
			except IndexError:
				headshot = ''
			# fetch author name
			try:
				regexAuthorName = re.compile(r"'full-name'>(.*?)</div>", re.DOTALL)
				AuthorName = re.findall(regexAuthorName, source)[0]
			except IndexError:
				AuthorName = ''
			# fetch Twitter Handle
			try:
				regexTwitter = re.compile("'twitter-handle'>.*?target=\"_blank\">(.*?)</a>", re.DOTALL)
				twitter = re.findall(regexTwitter, source)[0]
			except IndexError:
				twitter = ''
			# fetch Content Body HTML
			regexBody = re.compile("<div itemprop='articleBody' style='clear:both'>\n(.*?)</div>", re.DOTALL)
			body = re.findall(regexBody, source)[0]
			# clean up required for csv
			body = re.sub("\r\n"," ",body)
			body = re.sub("\n"," ",body)
			# write to csv file, using pipe deliminator
			output_csv.write('"'+datetime+'"|'+'"'+headline+'"|'+'"'+headshot+'"|'+'"'+AuthorName+'"|'+'"'+twitter+'"|'+'"'+body+'"\n')
			# download first image from article
			regexPicture = re.compile(r"<meta content=\"(.*?)\" name=\"twitter:image\"")
			picture = re.findall(regexPicture, source)[0]
			filename = "image_"+str(i)+".jpg"
			urr.urlretrieve(picture, filename)
output_csv.close()
