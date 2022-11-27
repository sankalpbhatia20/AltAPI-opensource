from selenium import webdriver
#from parsel import Selector
from selenium.webdriver.common.keys import Keys
import time

company = str(input('Enter company name: '))

# specifies the path to the chromedriver.exe
driver = webdriver.Chrome('/Users/sankalpbhatia/Downloads/chromedriver')

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com')

# locate email form by_class_name
username = driver.find_element('xpath', '/html/body/main/section[1]/div/div/form/div[2]/div[1]/input')
# send_keys() to simulate key strokes
username.send_keys('sankalpbhatia2003@outlook.com')

# locate password form by_class_name
password = driver.find_element('xpath', '/html/body/main/section[1]/div/div/form/div[2]/div[2]/input')
# send_keys() to simulate key strokes
password.send_keys('qwerty@2003')

# locate submit button by_class_name
log_in_button = driver.find_element('xpath', '/html/body/main/section[1]/div/div/form/button')

# .click() to mimic button click
log_in_button.click()

time.sleep(2)

# locate search button
search_button = driver.find_element('xpath', '/html/body/div[5]/header/div/div/div/div[1]/input')
# .click() to mimic button click
search_button.send_keys(company)
search_button.sendKeys(Keys.RETURN)

# clicking the first result we get
first_result = driver.find_element('/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/div/div/a/div/div[1]/div[1]/div/div')
first_result.click()