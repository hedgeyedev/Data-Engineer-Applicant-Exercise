from lxml import html, etree
import requests
import csv


page = requests.get('https://app.hedgeye.com/insights/all?type=insight')
tree = html.fromstring(page.content)

articles = tree.xpath('//div[@class="thumbnail-article"]'
	+ '/a[@class="thumbnail-article__title-link"]/@href')

with open('articles.csv', 'w') as csv_file:
	fieldnames = ['datetime', 'headline', 'author_name', 'author_image', 
		'author_twitter', 'content_html']
	writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
	writer.writeheader()

	for i, article in enumerate(articles):
		if i == 6:
			break

		article_page = requests.get('https://app.hedgeye.com' + article)
		article_tree = html.fromstring(article_page.content)

		datetime = article_tree.xpath('(//time/span)[2]/text()')[0]
		headline = article_tree.xpath('//h1[@itemprop="name"]/text()')[0]
		headline = headline.replace('\n', '')

		bylines = article_tree.xpath('//div[contains(@class, "bylines")]'
			+ '/div[contains(@class, "byline")]')
		if bylines:
			author_name = bylines[0].xpath('//div[@class="full-name"]'
				+ '/text()')[0]
			author_image = bylines[0].xpath('//div[@class="headshot"]'
				+ '/img/@src')[0]
			author_twitter = bylines[0].xpath('//div[@class="twitter-handle"]'
				+ '/a/text()')[0]
		else:
			author_name = 'n/a'
			author_image = 'n/a'
			author_twitter = 'n/a'

		body_tree = article_tree.xpath('//div[@itemprop="articleBody"]')
		content_html = b''
		for elem in body_tree:
			content_html += etree.tostring(elem)

		writer.writerow({
			'datetime': datetime,
			'headline': headline,
			'author_name': author_name,
			'author_image': author_image,
			'author_twitter': author_twitter,
			'content_html': content_html
		})

		# extra credit
		first_image_url = article_tree.xpath('(//div[@itemprop="articleBody"]'
			+ '/p/a/img)[1]/@src')
		if first_image_url:
			image = requests.get('https:' + first_image_url[0]).content
			with open('../images/image_' + str(i+1) + '.png', 'wb') as img_file:
				img_file.write(image)