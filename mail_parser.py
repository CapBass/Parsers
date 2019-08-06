from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
driver = webdriver.Firefox()

driver.get('https://mail.ru')
assert "Mail.ru" in driver.title

# Заполняем поля для ввода
elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('example_address@mail.ru')
elem = driver.find_element_by_id("mailbox:password")
elem.send_keys('just_password1')
elem.send_keys(Keys.RETURN)

wait = WebDriverWait(driver, 10)

wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'llc__content')))

letters = driver.find_elements_by_class_name('llc__content')

print(len(letters))
print(letters)
#driver.close()
