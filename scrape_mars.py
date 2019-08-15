
# # Dependencies
# !pip install splinter
# !pip install selenium
# !pip install --user splinter
import requests
import re
from splinter import Browser
from bs4 import BeautifulSoup as bs

import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

   # Dictionary to hold all scraped data
   mars_data = {}
   # Browser initiate 
   browser = init_browser()
   
   #Latest Mars news
   url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
   browser.visit(url)
   html = browser.html
   soup = bs(html, 'html.parser')
   # Find fields and save to dict
   news_title = soup.find("div", {"class": "content_title"}).text
   news_p = soup.find("div", {"class": "article_teaser_body"}).text
   mars_data['news_title'] = news_title
   mars_data['news_p'] = news_p
   
   #JPL Mars Featured Image
   url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
   browser.visit(url_img)
   html = browser.html
   soup = bs(html, 'html.parser')
   # Find fields and save to dict
   for link in soup.findAll(id="full_image"):
      feature_image = link.get('data-fancybox-href')
   feature_image_url = "https://www.jpl.nasa.gov" + feature_image
   mars_data['feature_image_url'] = feature_image_url
   
   #Mars Weather
   url_wt='https://twitter.com/marswxreport?lang=en'
   browser.visit(url_wt)
   html = browser.html
   soup = bs(html, 'html.parser')
   # Find fields and save to dict
   weather= soup.find("p",{"class":"TweetTextSize"})
   mars_weather = " ".join(weather.find_all(text=True, recursive=False))
   mars_data['mars_weather'] = mars_weather
   
   #Mars facts
   url_tb='https://space-facts.com/mars/'
   # browser.visit(url_tb)
   tables=pd.read_html(url_tb)
   df=tables[1]
   mars_df=df.rename(columns={0:"Description",1:"value"})
   mars_df.set_index('Description', inplace=True)
   mars_df1=mars_df.replace('\n', '')
   mars_table=mars_df1.to_html()
   # save to global dict
   mars_data['mars_table'] = mars_table
   
   # New browser MARS HEMISPHERES 
   url_mh = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
   browser.visit(url_mh)
   html = browser.html
   soup = bs(html, "html.parser")
   # find fields
   img_url= soup.findAll("",{"class":"item"})
   hemisphere_image_urls=[]
   # Loop
   for img in img_url:
      title = img.find("h3").text
      img_link= img.find("a")["href"]
      images = "https://astrogeology.usgs.gov/" + img_link 
      browser.visit(images)
      html = browser.html
      soup=bs(html, "html.parser")
      download = soup.find("div", {"class":"downloads"})
      full_img = download.find("a")["href"]
      hemisphere_image_urls.append({"title": title, "img_url": full_img})
   # save to global dict
   mars_data["hemisphere_image_urls"]=hemisphere_image_urls
   #close browser
   browser.quit()
   return mars_data
   
   # Store mars_data into MongoDB


