from apps.nseindia.utils import write_data_to_csv
from config import settings
import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from typing import List
from webdriver_manager.chrome import ChromeDriverManager


def get_data(url: str) -> List[tuple]:
    # Не забываем применить опции
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=settings.options)

    driver.get(url)
    driver.maximize_window()
    time.sleep(1)  # Даем немного прогрузиться

    market_data = driver.find_element(by=By.ID, value="link_2")  # Список с нужным элементом

    # Делаем наведение по тз;
    action = ActionChains(driver)
    action.move_to_element(market_data)
    action.perform()

    market_data.click()

    po = driver.find_element(by=By.LINK_TEXT, value="Pre-Open Market")
    po.click()
    time.sleep(1)

    dropdown = driver.find_element(by=By.ID, value="sel-Pre-Open-Market")
    action.move_to_element(dropdown)
    action.perform()
    dropdown.click()

    option = driver.find_element(by=By.ID, value="all")
    option.click()

    # js скрипт инициатор при клике на опцию со всеми данными отправляет запрос на АПИ с нужными токенами
    driver.execute_script('arguments[0].click();', option)
    time.sleep(settings.MAX_AWAIT_TIME)  # js делает запрос на который уходит некоторое время; можно поменять

    # Разбор подгруженных элементов
    table = driver.find_element(by=By.ID, value="livePreTable")
    raw_text = table.text  # Почему-то строки доступны только после обращения к webdriver элементу
    tuples = table.find_elements(by=By.TAG_NAME, value="tr")

    data = []
    for item in tuples[1:]:
        full = item.text.strip().split()  # Строка полностью
        name = full[0]
        if name != "Total":
            final = full[5]
            row = (name, final)
            data.append(row)

    time.sleep(1)
    return data


def main() -> None:
    main_url = "https://www.nseindia.com/"
    table_headers = ("Имя", "цена")
    counter = 0

    while True:
        try:
            data = get_data(main_url)
            write_data_to_csv(settings.NSEINDIA_FILE_PATH, data, table_headers)
            break
        except Exception as e:
            print(f"[WARNING] {datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")} {e}")
            if counter >= settings.MAX_RETRIES:
                break
            counter += 1
