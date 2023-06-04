import random
import os
import time
import requests

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# intialize google chrome browser

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless = new')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(
    'chromedriver',
    options = chrome_options
)

# # Create a empty folder for storing articles
root_dir = './vn_news_corpus'
os.makedirs(root_dir, exist_ok=True)
n_pages = 10 # change if want more articles
article_id = 0

for page_idx in range (n_pages):
    # Access page
    main_url = f'https://vietnamnet.vn/thoi-su-page{page_idx}'
    driver.get(main_url)
    
    # Get list
    news_lst_xpath = '//div[@class="topStory-15nd"]/div/div[1]/a'
    news_tags = driver.find_elements(
        By.XPATH,
        news_lst_xpath
    )
    news_page_urls = [
        news_tag.get_attribute('href') \
            for news_tag in news_tags
    ]
    for news_page_url in news_page_urls:
        # Access to article page
        driver.get(news_page_url)
        time.sleep(1)
        
        # Try to get main content tag
        main_content_xpath = '//div[@class="content-detail"]'
        try:
            main_content_tag = driver.find_element(
                By.XPATH,
                main_content_xpath
            )
        except:
            continue
        # ignore video
        video_content_xpath = '//div[@class="video-detail"]'
        try:
            video_content_tag = main_content_tag.find_element(
                By.XPATH,
                video_content_xpath
            )
            continue
        except:
            pass
        # Get title (h1 tag)
        title = main_content_tag.find_element(
            By.TAG_NAME,
            'h1'
        ).text.strip()
        
        # Get abstract (h2 tag)
        abstract = main_content_tag.find_element(
            By.TAG_NAME,
            'h2'
        ).text.strip()
        
        # Get author name (span tag)
        try:
            author_xpath = '//span[@class="name"]'
            author = main_content_tag.find_element(
                By.XPATH,
                author_xpath
            ).text.strip()
        except:
            author = ''
        # Get paragraphs (all p tags in div "maincontent main-content")
        paragraphs_xpath = '//div[@class="maincontent main-content"]/p'
        paragraphs_tags = main_content_tag.find_elements(
            By.XPATH,
            paragraphs_xpath
        )
        
        # Save content to a txt file
        paragraphs_lst = [
            paragraphs_tag.text.strip() \
                for paragraphs_tag in paragraphs_tags
        ]
        paragraphs = ' '.join(paragraphs_lst)
        # combine title, abstract, author and paragraphs
        final_content_lst = [title, abstract, paragraphs, author]
        final_content = '\n\n'.join(final_content_lst)
        
        # Save article to txt file
        article_filename = f'article_{article_id:05d}.txt'
        article_savepath = os.path.join(
            root_dir,
            article_filename
        )
        article_id += 1
        with open(article_savepath, 'w') as f:
            f.write(final_content)
        
        # Move back to previous page
        driver.back()