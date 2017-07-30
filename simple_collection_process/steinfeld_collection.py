import lxml
import requests
import scraperwiki
import urllib

#Sam Steinfeld
#Written and tested in Python 2.7
#lxml, requests, and scraperwiki were manually installed using 'pip install'

NUMARTICLES = 6 #number of articles to collect data from

def main():
      page = scraperwiki.scrape('https://app.hedgeye.com/insights/all?type=insight') #url of webpage
      root = lxml.html.fromstring(page)
      articles = root.xpath('//h2[@class="article-listing__heading"]/text()') #list of titles
      
      #collect references to articles
      hrefs = root.xpath('//a[@class="popular-this-week__heading--link"]')
      hrefs += root.xpath('//a[@class="latest-insights__heading--link"]')
      
      #create arrays for each piece of information to be collected from
      datetimes = []
      headshotRef = []
      names = []
      twitterhandles = []
      contentBodies = []
      
      imgNum = 1 #counter for total number of images
      
      #iterate through each article
      for href in hrefs[:NUMARTICLES]:
            link = scraperwiki.scrape('https://app.hedgeye.com/' + href.attrib['href'])      
            rootLink = lxml.html.fromstring(link)
            
            #datetime is the 41st element using span tag
            datetime = rootLink.xpath('//span/text()')
            datetimes.append(datetime[41])
            
            #collect each pice of information from each article and append to respective array
            img = rootLink.xpath('//div[@class="headshot"]//img/@src')  
            headshotRef.append(img) 
            name = rootLink.xpath('//div[@class="full-name"]/text()')
            names.append(name)  
            twitterhandle = rootLink.xpath('//div[@class="twitter-handle"]//a[@target="_blank"]/text()')
            twitterhandles.append(twitterhandle)            
            contentBody = rootLink.xpath('//div[@itemprop="articleBody"]//p//text()')
            contentBodies.append(contentBody)
            
            #collect only the first image from each article
            bodyHrefs = rootLink.xpath('//div[@itemprop="articleBody"]//a/@href')
            if bodyHrefs:
                  for ref in bodyHrefs:
                        if ref.endswith(('.png', 'jpg')):
                              urllib.urlretrieve(ref, "image" + str(imgNum) + ".jpg")
                              imgNum += 1                              
                              break
      
      output = open("./excel_output.csv", "w+") #create excel file
      
      #write each piece of information from respective array to excel file
      output.write("%s" % ("Datetimes:"))
      output.write("%c" % (",")) 
      for date in datetimes:
                  output.write("%s" % (date))
                  output.write("%c" % (","))    
      output.write("%c" % ("\n"))
      output.write("%s" % ("Article Titles:"))
      output.write("%c" % (",")) 
      
      for article in articles:
            article = article.replace(',', '')
            output.write("%s" % (article.encode('utf-8').strip()))
            output.write("%c" % (","))
      output.write("%c" % ("\n"))
      
      output.write("%s" % ("Author Headshot Links:"))
      output.write("%c" % (",")) 
      for headshot in headshotRef:
            if headshot: #check to see if array has any data
                  output.write("%s" % (headshot[0]))
            output.write("%c" % (","))
      output.write("%c" % ("\n"))
      
      output.write("%s" % ("Author Name:"))
      output.write("%c" % (",")) 
      for authorName in names:
            if authorName:
                  output.write("%s" % (authorName[0]))
            output.write("%c" % (","))  
      output.write("%c" % ("\n"))
      
      output.write("%s" % ("Twitter Handle:"))
      output.write("%c" % (",")) 
      for handle in twitterhandles:
            if handle:
                  output.write("%s" % (handle[0]))
            output.write("%c" % (","))  
      output.write("%c" % ("\n"))      
      
      
      output.write("%s" % ("Content Body:"))
      output.write("%c" % (",")) 
      for content in contentBodies:
            string = ""
            for c in content:
                  string += c.encode('utf-8').strip()
                  string += " "
            string = string.replace(',', ' ')
            output.write("%s" % (string))
            output.write("%c" % (","))  
      
      output.close()
# --- end main() ---------


#---------------------------------------------------------
# Python starts here ("call" the main() function at start
if __name__ == '__main__':
      main()
#---------------------------------------------------------  