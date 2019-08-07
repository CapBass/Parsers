from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from pymongo import MongoClient
import pymongo

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['mail']
mail_db = db.mail_ru
mail_db.create_index('letter_id', unique=True)

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
try:
    wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "js-letter-list-item")]')))
except TimeoutException:
    print('The page is loading too much')

letters = driver.find_elements_by_xpath('//a[contains(@class, "js-letter-list-item")]')

time.sleep(1) # доп. секунда, чтобы одолеть ктулху загрузочного экрана

for i in range(len(letters)):
    letters = driver.find_elements_by_xpath('//a[contains(@class, "js-letter-list-item")]')
    elem = letters[i]
    letter_id = elem.get_attribute('data-uidl-id')
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
    mail_data = {
        'letter_id': letter_id,
        'header': {
            'author': author,
            'date': date,
            'theme': theme
        },
        'text': text
    }
    try:
        mail_db.insert_one(mail_data)
        print(f'Record {letter_id} added')
    except pymongo.errors.DuplicateKeyError:
        print(f'Record {letter_id} already exist')
        continue

driver.close()
