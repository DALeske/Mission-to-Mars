# # CHALLENGE 10

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the Mars NASA news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div',class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()


# # STARTER CODE

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()

# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

### Hemispheres

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

# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)

# 5. Quit the browser
browser.quit()


