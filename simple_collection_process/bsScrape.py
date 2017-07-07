import requests, bs4, os, tqdm, datetime
import tkinter as tk, pandas as pd
from tkinter import filedialog
from dateutil import parser
from urllib import request

def scrape(url="https://app.hedgeye.com/insights/all?type=insight"):
	links = getLinks(url)
	filename = setFilename()
	list_=[]
	df = createDataFrame()														# provides a database friendly interface
	print("Generating CSV and downloading available images into directory...")
	for link in tqdm.tqdm(links[:6]):											# generates progress bar as the program writes each link to file
		df = writeToFolder(link,filename,df)
def createList(soup,h1,article):
	a = getAuthor(soup)															# returns author tuple containing image, name, and twitter handle
	list_ = [getTime(soup),h1,a[1],a[0],a[2],articleText(article)]				# [time, title, author_name, author_img, twitter handle, content]
	return list_
def createDataFrame():
	columns = ['date_published','title','author','author_img','author_twitter','content']	
	df = pd.DataFrame(columns = columns)										# create DataFrame with columns
	return df
def writeToFolder(link,filename,df):
	soup = getSoup(link)
	article = soup.find('div',{'itemprop':'articleBody'})						# gets body element
	h1 = soup.find('h1',{'itemprop':'name'}).getText()							# gets title from body
	h1 = stripStr(h1)
	list1 = createList(soup,h1,article)
	df.loc[len(df)] = list1														# adds a row to DataFrame
	df.to_csv(filename)															# write DataFrame to csv (rewrites if necessary)
	folder = os.path.split(filename)[0]
	writeImgToFile(folder,article)
	return df
def setFilename():
	folder = getFolderpath()
	now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
	filename = os.path.join(folder,"scrape"+now+".csv")							# writes to one csv with timestamp
	return filename
def stripStr(s):																
	str = s.rstrip()															# title needs newlines to be stripped on either side
	str = str.lstrip()
	return str
def writeImgToFile(folder,article):
	img = getImage(article)														# getImage returns [image url, image name]
	if img is not None:
		f = open(os.path.join(folder,img[1]+".jpg"),'wb')
		f.write(request.urlopen(img[0]).read())									# opens image url as bytestream -> writes to file
		f.close()	
def getImage(article):
	imgs = article.find_all('img')												# it just so happens that the first img with a src attribute is the one we're looking for
	for img in imgs:
		if img.has_attr('src'):
			return ["https:"+img['src'],replaceUnwantedChar(img['alt'])]
def articleText(article):
	text = ""
	raw_para = article.find_all('p')											# gets all <p> content within article. No headings for now.
	for para in raw_para:
		if para.getText() is not "":
			text = text + para.getText() + "\n"
	return text
def getAuthor(soup):
	author_info =[]
	author_headshot = soup.find('div',{'class':'headshot'})						# author image is found by attribute 'headshot'
	if author_headshot is not None:
		author_img = author_headshot.find('img')
		author_info.append(author_img['src'])
	else:
		author_info.append("")
	author_name = soup.find('div',{'class':'full-name'})						# author name is found by attribute 'full-name'
	if author_name is not None:
		author_info.append(author_name.getText())
	else:
		author_info.append("")
	author_twitter = soup.find('div',{'class':'twitter-handle'})				#author twitter handle is found by attribute 'twitter-handle'
	if author_twitter is not None:
		author_info.append(author_twitter.find('a',href = True).getText())
	else:
		author_info.append("")
	return author_info
def getTime(soup):
	time = soup.find('time',{'itemprop':'datePublished'})						# there are several <time> elements, the pertinent one has attribute 'datePublished'
	time_spans = time.find_all('span')
	time_  = time_spans[1]														# the correct time tag is found by choosing the second span
	return time_.text
def getSoup(url):
	data = requests.get(url,cookies=addCookies())								# needs acceptable cookies to avoid paywall
	soup = bs4.BeautifulSoup(data.content,"lxml")								# returns a dict that is easy to search
	return soup
def getLinks(url):
	soup=getSoup(url)
	content = soup.find('div',{'id':'content-container'})						# luckily, all links found in 'content-container' are the only ones we need
	raw_links = content.find_all('a',href = True)
	links=[]
	for link in raw_links:
		mod_link="https://app.hedgeye.com"+link["href"]							# links found do not contain the domain
		links.append(mod_link)
	return links
def writeSoupToFile(soup):
	folderPath=getFolderpath()
	f = open(os.path.join(folderPath,"soup.html"),'wb')
	f.write(soup.prettify(encoding='utf-8'))
	f.close()
def getFolderpath():
	root = tk.Tk()
	root.withdraw()
	root.update()
	file_path = filedialog.askdirectory()
	return file_path
def addCookies():
	jar = requests.cookies.RequestsCookieJar()									# cookies were needed to avoid paywall
	jar.set('_hedgeye_session', '3aae7d921022b89f5bf234a572616d34',   domain='.hedgeye.com', path='/')
	jar.set('_gid', 'GA1.2.341995985.1499002730',   domain='.hedgeye.com', path='/')
	jar.set('_ga', 'GA1.2.449954818.1498729384',   domain='.hedgeye.com', path='/')
	jar.set('customer_type', 'PremiumInsighter',   domain='.hedgeye.com', path='/')
	jar.set('signup_id', '7509',   domain='.hedgeye.com', path='/')
	jar.set('shopping_cart', '%7B%22timestamp%22%3A1499040499000%7D',   domain='.hedgeye.com', path='/')				

	return jar
def parseDatetime(s):
	s_ = parser.parse(s).strftime('%B %d, %Y, %H:%M:%S')
	return s_
def replaceUnwantedChar(str):
	for ch in ['|',':',')','\\','/','!','.','+','\'','\"','\n','?','!','>','(']:
		if ch in str:
			str=str.replace(ch,"_")
	return str