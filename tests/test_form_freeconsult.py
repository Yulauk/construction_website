# import time
import nltk
# from nltk.tokenize import word_tokenize
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import app


# Download NLTK data
nltk.download('punkt')
languages = ['en', 'et', 'uk', 'ru']
link = f'http://192.168.18.9:5000/{languages[0]}/'
browser = webdriver.Chrome()
browser.get(link)

# Find the form elements
name_field = browser.find_element(By.CSS_SELECTOR, 'input[name*=name-free-consult]')
contact_field = browser.find_element(By.CSS_SELECTOR, 'input[name*=contact-free-consult]')
comment_field = browser.find_element(By.CSS_SELECTOR, 'textarea[name*=comment-free-consult]')

# Fill in the form fields with the required information
name_field.send_keys('Selenium_tst')
contact_field.send_keys('380887778878')
comment_field.send_keys('selenium test')

# Scroll to the free consultation button
free_consult_button = (WebDriverWait(browser, 10).
                       until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class*=button-free-consult]'))))
actions = ActionChains(browser)
actions.move_to_element(free_consult_button).perform()

# Click the free consultation button
free_consult_button.click()

# Check the status
try:
    status_element = (WebDriverWait(browser, 10).
                      until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.alert-success'))))
    # status = status_element.text
    # print('status', status)
    # if status == 'Your application has been successfully sent':
    print('test form consult success')
except Exception as e:
    print('Error occurred while checking status:', e)
browser.close()


# Delete the test data from the database
with app.app.app_context():
    app.delete_selenium_tst_free_consult()
