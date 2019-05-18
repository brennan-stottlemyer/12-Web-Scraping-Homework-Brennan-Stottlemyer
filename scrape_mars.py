from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time


scraped_data={}

def scrape():

    # In[3]:
    executable_path = {'executable_path': '/Users/bstottlemyer/Downloads/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)


    # In[4]:


    html = browser.html
    soup = bs(html, 'html.parser')

    news_article_title_div = soup.find('div', class_='content_title')
    news_article_description_div = soup.find('div', class_='rollover_description_inner')

    news_article_title = news_article_title_div.find('a')

    news_title = news_article_title.text
    news_p = news_article_description_div.text

    print(news_title)
    print(news_p)

    scraped_data["news_title"] = news_title
    scraped_data["news_p"] = news_p

    # In[5]:


    url = 'https://www.jpl.nasa.gov'
    page = '/spaceimages/?search=&category=Mars'
    browser.visit(url+page)


    # In[6]:


    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image_div = soup.find('div', class_='carousel_items')

    featured_image_article_div = featured_image_div.find('article')
    featured_image_style = featured_image_article_div['style']
    featured_image_jpg = featured_image_style[23:-3]

    featured_image_url = url+featured_image_jpg

    print(featured_image_url)

    scraped_data["featured_image_url"] = featured_image_url


    # In[7]:


    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)


    # In[8]:


    html = browser.html
    soup = bs(html, 'html.parser')

    tweet_div = soup.find('p', class_='tweet-text')

    mars_weather_text = tweet_div.text

    if "pic.twitter.com" in mars_weather_text:
        mars_weather_split = mars_weather_text.split('pic.twitter')
        mars_weather = mars_weather_split[0]
        print(mars_weather)

    else:
        mars_weather = mars_weather_text
        print(mars_weather)

    scraped_data["mars_weather"] = mars_weather


    # In[9]:


    url = 'https://space-facts.com/mars/'
    browser.visit(url)


    # In[10]:


    tables = pd.read_html(url)
    tables


    # In[11]:


    df = tables[0]
    df.columns = ["Metric","Measurement"]
    df.set_index("Metric",inplace=True)
    df.head()


    # In[12]:


    html_table = df.to_html()
    html_table

    scraped_data["html_table"] = html_table

    # In[13]:


    hemisphere_image_urls = []


    # In[14]:


    url = 'https://astrogeology.usgs.gov'
    page = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    # In[15]:


    mars_hemisphere_pages = ['Cerberus Hemisphere Enhanced','Schiaparelli Hemisphere Enhanced','Syrtis Major Hemisphere Enhanced','Valles Marineris Hemisphere Enhanced']


    # In[16]:


    for hemisphere in mars_hemisphere_pages: 
        browser.visit(url+page)
        browser.click_link_by_partial_text(hemisphere)
        browser.click_link_by_partial_text('Open')

        html = browser.html
        soup = bs(html, 'html.parser')

        title_div = soup.find('h2', class_='title')
        cerberus_image_div = soup.find('img', class_='wide-image')

        title_text = title_div.text
        title = title_text.rsplit(' ', 1)[0]

        cerberus_image_src = cerberus_image_div['src']

        img_url = url+cerberus_image_src

        print(title)
        print(img_url)

        d = {"title":title,"img_url":img_url}
        hemisphere_image_urls.append(d)


    # In[23]:


    print(hemisphere_image_urls)

    scraped_data["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()

    return scraped_data
