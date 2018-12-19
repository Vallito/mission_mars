#import libraries
from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import time
import pandas as pd

#set up splinter browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

#visit url
url = "https://mars.nasa.gov/news/"
browser.visit(url)

#pull html text and parse
html_code = browser.html
soup = BeautifulSoup(html_code, "html.parser")


#print first news title
news_title = soup.find('div', class_= 'content_title').text

#print paragraph of news title
news_p = soup.find('div', class_='article_teaser_body').text
print(news_title)
print(news_p)

#visit url
featured_image_url= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(featured_image_url)

#pull html text and parse
test_code = browser.html
soup = BeautifulSoup(test_code, "html.parser")

#get image
browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(5)
browser.click_link_by_partial_text('more info')
time.sleep(10)
image_path = soup.find_all('img')[0]["src"]
featured_image_url = "https://www.jpl.nasa.gov/" + image_path

print(featured_image_url)

#scrape tweeter for mars data
mars_tweeter = 'https://twitter.com/marswxreport?lang=en'
browser.visit(mars_tweeter)
weather_html = browser.html
soup = BeautifulSoup(weather_html, 'html.parser')

mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(mars_weather)

mars_info = 'http://space-facts.com/mars/'

tables = pd.read_html(mars_info)
tables

df = tables[0]
html_table = df.to_html()

#collect title and image urls for each hemisphere
mars_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(mars_hemi)
hemi_html = browser.html
soup = BeautifulSoup(hemi_html,'html.parser')

hemispheres = ['Cerberus','Schiaparelli','Syrtis Major','Valles Marineris']
hemisphere_image_urls = []

for sphere in hemispheres:
    browser.click_link_by_partial_text(f"{sphere} Hemisphere Enhanced")
    time.sleep(3)
    website = browser.html
    new_soup = BeautifulSoup(website,'html.parser')
    hemi_source = new_soup.find_all('div', class_='downloads')[0]
    sphere_image = hemi_source.find_all('a')[0]['href']
    browser.click_link_by_partial_text('Back')
    title_image_urls = ({f"title: {sphere} Hemisphere, img_url: {sphere_image}"})
    hemisphere_image_urls.append(title_image_urls)

browser.quit()
print(hemisphere_image_urls)

    


