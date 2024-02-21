# import time
import nltk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import app


# Download NLTK data
nltk.download('punkt')
languages = ['en', 'et', 'uk', 'ru']
link = f'http://192.168.18.9:5000/{languages[0]}/'
browser = webdriver.Chrome()
browser.get(link)


# Find the form elements
# Find and interact with form elements
name = browser.find_element(By.CSS_SELECTOR, 'input[name*=name-contact-us]')
surname = browser.find_element(By.CSS_SELECTOR, 'input[name*=surname-contact-us]')
email = browser.find_element(By.CSS_SELECTOR, 'input[name=email-contact-us]')
phone = browser.find_element(By.CSS_SELECTOR, 'input[name=phone-contact-us]')
city = browser.find_element(By.CSS_SELECTOR, 'input[name*=city-contact-us]')
state = browser.find_element(By.CSS_SELECTOR, 'input[name*=state-contact-us]')
zip_code = browser.find_element(By.CSS_SELECTOR, 'input[name*=zip-contact-us]')
address = browser.find_element(By.CSS_SELECTOR, 'input[name*=address-contact-us]')
budget = browser.find_element(By.CSS_SELECTOR, 'select[name*=budget-contact-us]')
tim_e = browser.find_element(By.CSS_SELECTOR, 'select[name*=time-contact-us]')
source = browser.find_element(By.CSS_SELECTOR, 'select[name*=source-contact-us]')
project = browser.find_element(By.CSS_SELECTOR, 'textarea[name*=project-contact-us]')


# Fill in the form fields with the required information
name.send_keys('Selenium_tst')
surname.send_keys('Dev')
email.send_keys('selenium@test.com')
phone.send_keys('380887778878')
city.send_keys('Zurich')
state.send_keys('Zurrichberg')
zip_code.send_keys('03011')
address.send_keys('Bahnhofstrasse')
project.send_keys('selenium test')

# Selecting options from dropdown menus
budget_select = Select(budget)
tim_e_select = Select(tim_e)
source_select = Select(source)

# Selecting options by visible text
budget_select.select_by_value('$50,000-$99,999')
tim_e_select.select_by_value('3-months')
source_select.select_by_value('social')

# Scroll to and click the submit button
submit_button = browser.find_element(By.CSS_SELECTOR, 'button[class*=button-contact-us]')
actions = ActionChains(browser)
actions.move_to_element(submit_button).perform()
submit_button.click()


# Check the status
try:
    status_element = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.alert-success')))

    status = status_element.text
    print('status', status)
    if status == 'Your application has been successfully sent':
        print('test form contact success')
except Exception as e:
    print('Error occurred while checking status:', e)
browser.quit()


# Delete the test data from the database
with app.app.app_context():
    app.delete_selenium_tst_contact()
