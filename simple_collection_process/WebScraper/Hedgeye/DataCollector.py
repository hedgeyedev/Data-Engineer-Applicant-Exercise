from configparser import ConfigParser
from bs4 import BeautifulSoup
import urllib3
import urllib
import requests
from urllib.request import urlretrieve 

def collectData(content):
    listOfData = []

    content.prettify()

    #Get dateTime
    
    for i in content.findAll('time'):
        if i.has_attr('pubdate'):
            dateTime = i['datetime']
            if dateTime == "":
                listOfData.append("")
            else:
                listOfData.append(dateTime)
            
    #Get Headline
 
    headLine = content.findAll('h1', {"class":'se-headline headline_droid'})[0].get_text()
    if headLine == "":
        listOfData.append("")
    else:
        listOfData.append(headLine.replace("\n",""))
    
    #Get author details
    
    authorName = content.findAll('div', {"class":'full-name'})
    if len(authorName) == 0:
        listOfData.append("")
    else:
        listOfData.append(authorName[0].get_text())
    
    twitterHandle = content.findAll('div', {"class":'twitter-handle'})
    if len(twitterHandle) == 0:
        listOfData.append("")
    else:
        listOfData.append(twitterHandle[0].get_text().replace("@","").replace("\n",""))
    
    authorImageRef = content.findAll('img', {"alt":'Headshot mccullough'})
    if len(authorImageRef) == 0:
        listOfData.append("")
    else:
        listOfData.append(authorImageRef[0]["src"])
   
    #get content body HTML
    contentBody = body = content.find('div',{"itemprop":"articleBody"})
    #cont = contentBody.findChildren()
    listOfData.append(str(contentBody.findChildren()))
    
    return listOfData

    #save first image to file
    
def saveImageToLocalDisk(content,pathOfImage):
  
    insideBody = content.find('div',{"itemprop":"articleBody"})
    src = insideBody.find_all('img')[0]["src"]
    urllib.request.urlretrieve("http:"+src, pathOfImage)

def generateFile(pathOfFile,listOfData):
    file  = open(pathOfFile, "w")
    file.write("Datetime Published"+","+"Headline"+","+"Author_Name"+","+"Author_Twitter"+",""Author_Image_Ref"+","+"Content_Body_HTML"+"\n")
    for i in listOfData:
        file.write(i)
        file.write(",")
    file.close()
    
def main():
    config = ConfigParser()
    config.read('config.properties')
    linkToParse = config.get('LinkToParse', 'link')
    pathOfImage = config.get('Paths', 'pathOfImage')
    pathOfFile = config.get('Paths', 'pathOfFile')
    request = requests.get(linkToParse)
    request.content
    content = BeautifulSoup(request.content,'html.parser')
    listOfData = collectData(content)
    saveImageToLocalDisk(content,pathOfImage)
    generateFile(pathOfFile,listOfData)
    
if __name__ == '__main__':
    main()    