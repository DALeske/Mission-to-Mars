# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    browser.quit()

    browser = Browser('chrome', **executable_path, headless=True)
    hemisphere_image_urls = hemispheres(browser)
    browser.quit()

    browser = Browser('chrome', **executable_path, headless=True)
    featured_img = featured_image(browser)
    print(featured_img)
    
    

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_img,
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_image_urls
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    #print(img_url)
    return img_url


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")



def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    time.sleep(1)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    member = soup(html, "html.parser")

    hemi_items = member.find_all('div', class_='item')
    # get titles
    for items in hemi_items:  
        hemi_title = items.find('h3').text
    
        # get links to page with full image
        prelink = items.find('a')
        link = prelink['href']
        linkurl = f"{url}{link}"
    
        #visit linked page with the full image
        browser.visit(linkurl)
        time.sleep(0)
        # new scraping instance
        html = browser.html
        member2 = soup(html, "html.parser")

        # get url for full image (Option 1)
        hemi_image_div = member2.find('div', class_='downloads')
        hemi_image_prelink = hemi_image_div.find('a')['href']
        hemi_image_link = f"{url}{hemi_image_prelink}"
        
        # get url for full image (option 2)
        # hemi_image_div = member2.find('div', class_='wide-image-wrapper')
        # hemi_image_class = hemi_image_div.find('img',class_='wide-image')
        # hemi_image_prelink = hemi_image_class['src']
        # hemi_image_link = f"{url}{hemi_image_prelink}"
        
        # back up 1 page
        browser.back()
        # Create dictionary and append to list
        info_dict ={'img_url': hemi_image_link, 'title': hemi_title}
        hemisphere_image_urls.append(info_dict)
    

    # 5. Quit the browser
    browser.quit()
    return hemisphere_image_urls

if __name__ == "__main__":

# If running as script, print scraped data
    scrape_all()

 