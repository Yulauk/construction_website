import nltk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from langdetect import detect


# Download NLTK data
nltk.download('punkt')

languages = ['en', 'et', 'uk', 'ru']

for language in languages:
    link = f'http://192.168.18.9:5000/{language}/'
    browser = webdriver.Chrome()
    browser.get(link)
    wait = WebDriverWait(browser, 10)
    search_page_about = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.about-index')))
    search_page_about.click()

    check_h1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.page-set')))

    # scrolling to make the element accessible for interaction
    browser.execute_script("arguments[0].scrollIntoView();", check_h1)

    # ActionChains - selecting different actions using the mouse and keyboard on web pages
    actions = ActionChains(browser)

    actions.move_to_element(check_h1).click().perform()

    find_h1 = browser.find_element(By.CSS_SELECTOR, value='h1').text
    find_cv = browser.find_element(By.CSS_SELECTOR, value='div[class*=fst-italic]').text
    if detect(find_h1) == detect(find_cv):
        print('test about pass..')
    else:
        print(f'{find_h1[:10]} | {find_cv[:10]}')

    browser.close()




