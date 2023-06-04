import random
import pandas as pd
import os
import time
import re
import requests

from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("start-maximized")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disabled-dev-shm-usage")

driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install()),
    options = chrome_options
)

url = 'https://python.org/'
driver.get(url)
text = driver.find_element(
    By.XPATH,
    '/html/body/div/header/div/div[3]/p'
).text
print(text)