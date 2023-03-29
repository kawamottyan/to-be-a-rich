'''driverを設定する'''

import set_url

from selenium import webdriver
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium.webdriver.common.by import By

def open_chrome(URL):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    wait = WebDriverWait(driver, 3)
    driver.get(URL)
    time.sleep(1)
    wait.until(EC.presence_of_all_elements_located)
    return driver,wait