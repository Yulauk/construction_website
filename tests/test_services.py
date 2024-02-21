import nltk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from langdetect import detect


# Функция для проверки шагов на странице
def check_steps(browser):
    check_h1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.page-set')))
    browser.execute_script("arguments[0].scrollIntoView();", check_h1)

    actions = ActionChains(browser)
    actions.move_to_element(check_h1).click().perform()

    find_h1 = browser.find_element(By.CSS_SELECTOR, value='h1').text
    find_step_process = browser.find_element(By.CSS_SELECTOR, value='div.px-0').text

    find_step = [browser.find_element(By.CSS_SELECTOR, value='div.step-one').text,
                 browser.find_element(By.CSS_SELECTOR, value='div.step-two').text,
                 browser.find_element(By.CSS_SELECTOR, value='div.step-three').text,
                 browser.find_element(By.CSS_SELECTOR, value='div.step-four').text]

    find_step_text = [browser.find_element(By.CSS_SELECTOR, value='div.step-one-text').text,
                      browser.find_element(By.CSS_SELECTOR, value='div.step-two-text').text,
                      browser.find_element(By.CSS_SELECTOR, value='div.step-three-text').text,
                      browser.find_element(By.CSS_SELECTOR, value='div.step-four-text').text]

    print(f'{find_h1[:10]} | {find_step_process[:15]}')

    for i, ii in zip(find_step, find_step_text):
        if detect(i) == detect(ii):
            print('test services pass..\n')
        else:
            print(f'{detect(i)}({i[:16]})\n{detect(ii)}({ii[:16]})')


# Download NLTK data
nltk.download('punkt')

languages = ['en', 'et', 'uk', 'ru']

for language in languages:
    link = f'http://192.168.18.9:5000/{language}/'
    browser = webdriver.Chrome()
    browser.get(link)
    wait = WebDriverWait(browser, 10)
    search_page_services = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.about-services')))
    search_page_services.click()

    check_steps(browser)

    browser.quit()
