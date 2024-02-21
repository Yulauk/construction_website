import nltk
from selenium import webdriver
from selenium.webdriver.common.by import By
from langdetect import detect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Download NLTK data
nltk.download('punkt')

languages = ['en', 'et', 'uk', 'ru']
css_selectors_next_search_string = {
    'a.stages-of-plumbing-work': ['a.key-steps-in-electrical-installation', 'a.apartment-renovation', 'a.building-creation'],
    'a.comprehensive-electrical-installation-for-apartment-renovation': ['a.apartment-renovation', 'a.building-creation', 'a.key-steps-in-electrical-installation'],
    'a.apartment-renovation': ['a.stages-of-plumbing-work', 'a.key-steps-in-electrical-installation', 'a.building-creation'],
    'a.building-creation': ['a.stages-of-plumbing-work', 'a.apartment-renovation', 'a.key-steps-in-electrical-installation']
}

for language in languages:
    for css_selector, recent_posts in css_selectors_next_search_string.items():
        link = f'http://192.168.18.9:5000/{language}/'
        browser = webdriver.Chrome()
        browser.get(link)
        wait = WebDriverWait(browser, 10)
        search_string = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.about-blog')))
        search_string.click()

        next_search_string = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
        browser.execute_script("arguments[0].scrollIntoView();", next_search_string)

        actions = ActionChains(browser)
        actions.move_to_element(next_search_string).click().perform()

        h2 = browser.find_element(By.CSS_SELECTOR, value='h2').text
        description = browser.find_element(By.CSS_SELECTOR, value='p.blog-post-meta').text

        language_portfolio_name = detect(h2)
        language_portfolio_description = detect(description)

        if language == language_portfolio_name and language == language_portfolio_description:
            print(f'test BLOG language ({language}) passing')
        else:
            print(f"FILED BLOG lang must be('{language.upper()}')!\n{h2}\n"
                  f"{language}, {language_portfolio_name}, {language_portfolio_description}\n"
                  f"{description}")

        for post in recent_posts:
            recent_post_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, post)))
            browser.execute_script("arguments[0].scrollIntoView();", recent_post_element)
            actions = ActionChains(browser)
            actions.move_to_element(recent_post_element).click().perform()

        browser.quit()
