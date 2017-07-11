## For instructions please view README.md file
require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'fileutils'
require 'csv'
PAGE_URL = "https://app.hedgeye.com/insights/all?type=insight"
news_base_link = "https://app.hedgeye.com"

## Assigns the page that list articles.
page = Nokogiri::HTML(open(PAGE_URL))

## Assigns relative news link from PAGE_URL
news_links = page.xpath('//div[@class="article-listing"]/a/@href')

## EDGECASE: checks to see if 'scraped.csv' file exists
## to avoid duplicate appended data if script is ran more than once
if File.file?('scraped.csv')
    File.delete('scraped.csv')
end

# puts "TEST news_url article with author"
# news_url = "https://app.hedgeye.com/insights/56827-investors-positioned-for-a-correction-are-positioned-for-failure"

## Loops through 'news_links' from 'PAGE_URL'
i = 0
while i < 6
    # puts i
    news_relative_link = news_links[i]
    ## concatitantes links for usable 'news_url'
    news_url = news_base_link + news_relative_link
    ## assigns 'news_url' for nokogiri
    news = Nokogiri::HTML(open(news_url))
    ## column attributes for rows
    date_published = news.xpath('//time/span/text()')
    headline = news.xpath('//h1[@class="se-headline headline_droid"]/text()')
    author = news.xpath('//div[@class="full-name"]/text()')
    author_image = news.xpath('//div[@class="headshot"]/img/@src')
    author_twitter = news.xpath('//div[@class="twitter-handle"]/a/@href')
    body = news.xpath('//div[@itemprop="articleBody"]')
    ## EDGECASE: for news_link[0] because "articleBody" selector doesn't exist
    if body.size == 1
        ## pass
    else
        body = news.xpath('//div[@class="body"]')
    end
    ## assigns column atributes to row array
    row = [date_published, headline, author, author_image, author_twitter, body]
    puts "-------------------------------"
    puts "scraping article:"
    puts row[1]
    puts news_url
    puts "-------------------------------"
    # creates csv file
    CSV.open('scraped.csv', 'a') do |csv|
        ## appends row array to csv file
        csv << row
    end
    ## Extra Credit: Downloads First Image from meta data
    first_image = news.xpath('//meta[@property="og:image"]/@content')
    ## wget to download images
    %x'wget -N #{first_image}'
    ## /Extra Credit
    i += 1
end

puts "script complete check file ./scraped.csv"
