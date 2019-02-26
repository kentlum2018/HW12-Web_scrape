#Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import time

# Func to start splinter and assign Chrome as browser
# # executable_path = {'executable_path': 'chromedriver.exe'}
# I changed the CHROMEDRIVER!!! as per Ernest
executable_path = {"executable_path": "chromedriver"}
browser = Browser('chrome', **executable_path, headless=False)


#create SCRAPE func for html page
def scrape():
    # browser = init_browser()

    #create dict for holding all info
    mars_raw={}    
    ## Mars News

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)
    #scrape headline
    html=browser.html
    news_soup = bs(browser.html, 'lxml')
    # print(news_soup.prettify())
    time.sleep(2)
    #to pause 
    news_title = news_soup.find(class_='content_title', string=True)
    #print(news_title)
    time.sleep(2)
    #to pause
    news_p = news_soup.find(class_='article_teaser_body', string=True)
    # print(news_p)

    #add to dict
    mars_raw['cur_news_title']=news_title
    mars_raw['cur_news_p']=news_p

    #scrape images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url='https://www.jpl.nasa.gov'
    browser.visit(url)
    #click thru to get to final image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')

    #Create a Beautiful Soup object
    soup_img = bs(browser.html, 'lxml')

    #scrape final image
    news_img =soup_img.find(class_="main_image")
    # print(news_img)

    #full image URL
    featured_image_URL= base_url + news_img['src']
    #print(featured_image_URL)

    #add to dict
    main_image=news_img
    # mars_raw[image_1]=news_img
    # mars_raw[image_caption]=featured_image_URL
    image_txt=featured_image_URL

    ### Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    #Create a Beautiful Soup object
    soup_wea = bs(browser.html, 'lxml')
    # print(soup_wea.prettify())

    #scrape for twitter text
    twe_txt =soup_wea.find(class_="tweet-text")
    #print(twe_txt)

     #add to dict
    # mars_raw[wea_txt]=twe_txt
    wea_txt=twe_txt
    ### Mars Facts

    url = 'http://space-facts.com/mars/'
    browser.visit(url)

    #scrape table
    tables = pd.read_html(url)
    #format
    df = tables[0]
    df.columns = ['Component', 'Measurement']
    #     df.head()
    html_table = df.to_html(index=False)
    #     html_table
    html_table= html_table.replace('\n', '')
    #     html_table

    ### Mars Hemispheres
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)
    #use for loop to extract all the 4 hemispheres in a list
    # use the list then to pull all the 4 images 
    hemisphere_image_urls = []
    browser.visit(hemis_url)
    hemis_soup = bs(browser.html, 'lxml')
    hemis_query = hemis_soup.find_all(class_='item')
    for result in hemis_query:
        browser.visit(hemis_url)
        browser.click_link_by_partial_text(result.h3.text)
        hemis_temp_soup = bs(browser.html, 'lxml')
        hemi_name = result.h3.text.replace(' Enhanced', '')
        hemi_img_url = hemis_temp_soup.find(target='_blank')['href']
        hemisphere_image_urls.append({'title':hemi_name, 'img_url':hemi_img_url})
        #add to dict
        # mars_raw[hemi_img]=hemisphere_image_urls
        # hemi_img1=hemisphere_image_urls[0]
        # hemi_img2=hemisphere_image_urls[1]
        # hemi_img3=hemisphere_image_urls[2]
        # hemi_img4=hemisphere_image_urls[3]

    mars_raw = dict (
        cur_news_title =news_title,
        cur_news_p =news_p,
        # image_1 =news_img,
        image_1=main_image,
        image_caption = image_txt,
        tweet =wea_txt,
        html_table =html_table,
        hemi1 =hemisphere_image_urls
        # hemi2 =hemisphere_image_urls,
        # hemi3 =hemisphere_image_urls,
        # hemi4 =hemisphere_image_urls  
    )

    return mars_raw