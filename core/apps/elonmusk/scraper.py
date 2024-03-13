from config import settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from seleniumwire import webdriver as alterdriver
import time


def posts_handler(browser: webdriver, post_link: str) -> str:
    author = "elonmusk"
    domain = "https://twitter.com/"

    browser.get(post_link)
    time.sleep(settings.MAX_AWAIT_TIME)

    # Сбор текста
    text = "post with no text"
    if author not in post_link:
        author = "repost"
    try:
        text_div = browser.find_element(by=By.XPATH, value="//div[@class='css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-1inkyih r-16dba41 r-bnwqim r-135wba7']")
        text = text_div.text.strip().replace("\n", " ")
    except NoSuchElementException:
        pass

    # Поиск комментов: к сожалению фронтенд не дает фильтровать комменты по дате
    comments = browser.find_elements(by=By.XPATH, value="//a[@class='css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-xoduu5 r-1q142lx r-1w6e6rj r-9aw3ui r-3s2u2q r-1loqt21']")
    commentators = []
    for item in comments[0:3]:
        commentators.append(domain + item.get_attribute("href").split("/")[3])

    return f"Author: {author} Text: {text} Commentators: {', '.join(commentators)}"


def get_posts_links(browser: webdriver, login_view: str, elon_view: str) -> list[str]:
    # Login

    browser.maximize_window()
    browser.get(login_view)
    time.sleep(settings.MAX_AWAIT_TIME)  # Из-за проксирования скрипт может грузиться довольно долго

    input_field = browser.find_element(by=By.XPATH, value="//input[@autocomplete='username']")
    input_field.send_keys(settings.T_USERNAME)

    submit_button = browser.find_element(by=By.XPATH, value="//div[@class='css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-ywje51 r-usiww2 r-13qz1uu r-2yi16 r-1qi8awa r-ymttw5 r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l']")
    webdriver.ActionChains(browser).move_to_element(submit_button).click(submit_button).perform()
    time.sleep(settings.MAX_AWAIT_TIME)  # работает скрипт

    password_field = browser.find_element(by=By.XPATH, value="//input[@type='password']")
    password_field.send_keys(settings.T_PASSWORD)
    time.sleep(0.5)  # поле активируется только после ввода

    submit_button = browser.find_element(by=By.XPATH, value="//div[@class='css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-19yznuf r-64el8z r-1dye5f7 r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l']")
    webdriver.ActionChains(browser).move_to_element(submit_button).click(submit_button).perform()
    time.sleep(settings.MAX_AWAIT_TIME)

    # если поставить прокси с отличающимся от прошлого логина местоположением, выскочит двухфакторка
    try:
        verify = browser.find_element(By.XPATH, "//h1[@class='css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-1yjpyg1 r-ueyrd6 r-b88u0q']")
    except NoSuchElementException:
        verify = None
    if verify is not None:
        time.sleep(settings.MAX_VERIFY_TIME)  # достаточное время, чтобы ввести проверочный код | 60 s

    # Страница Илона Муска
    browser.get(elon_view)
    time.sleep(settings.MAX_AWAIT_TIME)
    point = browser.find_element(by=By.XPATH, value="//div[@class='css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-n6v787 r-1cwl3u0 r-16dba41 r-hrzydr r-j2kj52']")
    actions = ActionChains(browser)
    actions.move_to_element(point)

    # фронтенд построен хитро; посты загружаются динамически и каждый скролл меняет состояние элементов;
    # т.е на место старых постов грузятся новые и на странице активны всегда 5 - 15 постов не более;
    # настроил скролл ниже, что грузит именно последние 8 - 15 постов;
    for i in range(10):
        pix = random.randint(150, 250)
        browser.execute_script(f"window.scrollBy(0, {pix});")
        time.sleep(1)
    # через прокси во время теста все жестко тормозило, дадим больше
    time.sleep(random.randint(5, 10))  # чтобы все посты подгрузились;

    posts = browser.find_elements(by=By.XPATH, value="//a[@class='css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-xoduu5 r-1q142lx r-1w6e6rj r-9aw3ui r-3s2u2q r-1loqt21']")
    settings.stream_logger.debug(msg=f"Posts count: {len(posts)}")

    links = []
    for item in posts:
        links.append(item.get_attribute("href"))

    return links


def main():
    counter = 0
    login = "https://twitter.com/i/flow/login/"
    elon = "https://twitter.com/elonmusk/"

    if settings.PROXY:
        proxy_options = settings.seleniumwire_options

        driver = alterdriver.Chrome(
            options=settings.options,
            seleniumwire_options=proxy_options)
    else:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=settings.options)

    while True:
        try:
            links = get_posts_links(driver, login, elon)
            for link in links:
                message = posts_handler(driver, link)
                settings.file_logger.info(msg=message)
                settings.stream_logger.debug(msg=f"GET MESSAGE FROM {link}: SUCCESS")
            settings.stream_logger.debug(msg=f"ALL MESSAGES ARE SUCCESSFULLY RECEIVED")
            break
        except Exception as e:
            settings.stream_logger.warning(msg=f"EXCEPTIONS RAISES: {e}")
            if counter >= settings.MAX_RETRIES:
                break
            counter += 1

    driver.close()
