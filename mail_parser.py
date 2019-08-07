from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re

driver = webdriver.Firefox()

driver.get('https://mail.ru')
assert "Mail.ru" in driver.title

# Заполняем поля для ввода
elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('example_address@mail.ru')
elem = driver.find_element_by_id("mailbox:password")
elem.send_keys('just_password1')
elem.send_keys(Keys.RETURN)

wait = WebDriverWait(driver, 25)

wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "js-letter-list-item")]')))

letters = driver.find_elements_by_xpath('//a[contains(@class, "js-letter-list-item")]')

time.sleep(1)

for i in range(len(letters)):
    letters = driver.find_elements_by_xpath('//a[contains(@class, "js-letter-list-item")]')
    elem = letters[i]
    elem.click()
    elem = driver.find_element_by_xpath('//span[contains(@class, "letter__contact")]')
    author = elem.get_attribute('title')
    elem = driver.find_element_by_class_name('letter__date')
    date = elem.text
    elem = driver.find_element_by_class_name('thread__subject')
    theme = elem.text
    elem = driver.find_element_by_class_name('letter__body')
    text = ' '.join(elem.text.split())
    elem = driver.find_element_by_class_name('button2__txt')
    elem.click()
    print(theme)


driver.close()
