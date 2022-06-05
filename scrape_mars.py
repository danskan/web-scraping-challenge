# imports

from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

# scrape all function
def scrape_all():
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    
    
    
    
    news_title, news_paragraph = scrape_news(browser)

    mars_data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': scrape_feature_img(browser),
        'facts': scrape_facts(browser),
        'hemispheres': scrape_hemispheres(browser),
        'last_updated': dt.datetime.now()
    }

    browser.quit()

    return mars_data




# scrape mars news page
def scrape_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)



    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = bs(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    news_title = slide_elem.find('div', class_='content_title').get_text()

    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    return news_title, news_p

# scrape featured image page
def scrape_feature_img(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    full_image_link = browser.find_by_tag('button')
    full_image_link[1].click()
    html = browser.html
    img_soup = bs(html, 'html.parser')
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

#  scrape facts page
def scrape_facts(browser):
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    html = browser.html
    fact_soup = bs(html, 'html.parser')
    facts_loc = fact_soup.find('div', class_='diagram mt-4')
    fact_table = facts_loc.find('table')
    facts = ''
    facts += str(fact_table)
    return facts

# scrape hemispheres page
def scrape_hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # create a list to hold the images and title
    hemisphere_image_urls = []
    for i in range(4):
        hemisphereInfo = {}
        browser.find_by_css('a.product-item img')[i].click()
        sample = browser.links.find_by_text('Sample').first
        hemisphereInfo['img_url'] = sample['href']
        hemisphereInfo['title'] =browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemisphereInfo)
        browser.back()
    return hemisphere_image_urls

# stop the webdriver
    

# set up as a flask app

if __name__ == "__main__":
    print(scrape_all())