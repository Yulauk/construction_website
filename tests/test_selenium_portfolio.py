# import time
import nltk
from selenium import webdriver
from selenium.webdriver.common.by import By
from langdetect import detect


# Download NLTK data
nltk.download('punkt')
languages = ['en', 'et', 'uk', 'ru']
css_selectors_next_search_string = ['img.ESTONIAN-ACADEMY', 'img.COMPREHENSIVE-RENOVATION', 'img.HOME-CINEMA5']
css_selectors_description = ['p.academy-music', 'p.varshavsky-residential', 'p.cinematic5']

for language in languages:
    for css_selector, css_selectors_p in zip(css_selectors_next_search_string, css_selectors_description):
        link = f'http://192.168.18.9:5000/{language}/'
        browser = webdriver.Chrome()
        browser.get(link)
        search_string = browser.find_element(By.CSS_SELECTOR, 'div.container-bottom-corusel')
        search_string.click()

        next_search_string = browser.find_element(By.CSS_SELECTOR, value=css_selector)
        next_search_string.click()

        h1 = browser.find_element(By.CSS_SELECTOR, value='h1').text
        description = browser.find_element(By.CSS_SELECTOR, value=css_selectors_p).text

        # Language detection
        language_portfolio_name = detect(h1)
        language_portfolio_description = detect(description)
        # print(language, language_portfolio_name, language_portfolio_description)
        if language == language_portfolio_name and language == language_portfolio_description:
            print(f'test ESTONIAN-ACADEMY language ({language}) passing')
        else:
            print(f"FILED ESTONIAN-ACADEMY lang must be('{language.upper()}')!\n>>> {h1}\n"
                  f"{language}, {language_portfolio_name}, {language_portfolio_description}")

        browser.quit()
