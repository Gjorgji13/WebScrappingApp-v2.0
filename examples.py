from bs4 import BeautifulSoup
import requests
url = 'https://example.com'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
titles = soup.find_all('h1')
for title in titles:
    print(title.text)




import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
            }



from selenium import webdriver
driver = webdriver.Chrome()
driver.get('http://example.com')
title = driver.find_element_by_tag_name('h1').text
print(title)
driver.quit()
