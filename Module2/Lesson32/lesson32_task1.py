"""Lesson32 Task1: Implementation the Web Scraper."""

import os
import time
import random
import requests

from bs4 import BeautifulSoup
from requests import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
    TimeoutException,
)
from tqdm import tqdm


def create_folder_if_not_exists(folder_path):
    """
    Создаёт папку по указанному пути, если она ещё не существует.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def init_driver(geckodriver_path, headless=False):
    """
    Инициализирует и возвращает объект Selenium WebDriver для Firefox.
    """
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("--headless")

    service = Service(geckodriver_path)
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def get_thumbnail_urls(
    query, limit=10, delay=3, headless=False, geckodriver_path=None, base_url=None
):
    """
    Ищет изображения (миниатюры) по запросу 'query' на Яндекс Картинках,
    возвращая не более 'limit' уникальных URL на миниатюры.
    """
    # Инициализируем драйвер
    try:
        driver = init_driver(geckodriver_path, headless)
    except WebDriverException as e:
        print("Ошибка при запуске Firefox WebDriver:", e)
        return []

    # Формируем URL для Яндекс.Картинок
    params = {"text": query}
    request_url = Request("GET", base_url, params=params).prepare().url

    # Переходим по URL
    driver.get(request_url)

    # Явное ожидание появления основных элементов
    print("Ждём появления картинок...")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "ImagesContentImage-Image")
            )
        )
        print("Картинки успешно загрузились!")
    except TimeoutException:
        print("Не удалось дождаться загрузки страницы с результатами.")
        driver.quit()
        return []

    collected_urls = set()  # Чтобы избежать дублирования
    stop_scrolling = False

    while len(collected_urls) < limit and not stop_scrolling:
        # Проверяем, не застряли ли мы на капче
        if "showcaptcha" in driver.current_url:
            print("Обнаружена капча! Решите её вручную...")
            # Пока пользователь не введёт капчу, мы в паузе
            while "showcaptcha" in driver.current_url:
                time.sleep(5)

        # Парсим текущую страницу
        soup = BeautifulSoup(driver.page_source, "lxml")
        image_tags = soup.find_all("img", class_="ImagesContentImage-Image")

        for img_tag in image_tags:
            thumb_url = img_tag.get("src")
            if not thumb_url:
                continue

            # Если ссылка начинается с '//', добавляем 'https:'
            if thumb_url.startswith("//"):
                thumb_url = "https:" + thumb_url

            if thumb_url not in collected_urls:
                collected_urls.add(thumb_url)
                if len(collected_urls) >= limit:
                    break

        # Если уже набрали нужное число ссылок, выходим
        if len(collected_urls) >= limit:
            break

        # Прокрутка вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(delay, 2 * delay))

        # Пытаемся нажать «Показать ещё» (если есть)
        try:
            show_more_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'FetchListButton')]//button[contains(@class, 'Button2')]",
                    )
                )
            )
            show_more_button.click()
            time.sleep(random.randint(delay, 2 * delay))
        except (TimeoutException, NoSuchElementException):
            # Нет кнопки «Показать ещё» или она не кликабельна
            stop_scrolling = True

    driver.quit()
    return list(collected_urls)[:limit]


def download_images(image_urls, target_folder):
    """
    Скачивает переданные URL (image_urls) как файлы .jpg в папку target_folder,
    давая им имена с ведущими нулями.
    """
    create_folder_if_not_exists(target_folder)

    for idx, url in enumerate(tqdm(image_urls, desc=f"Скачиваем в {target_folder}")):
        filename = f"{str(idx).zfill(4)}.jpg"
        file_path = os.path.join(target_folder, filename)

        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(resp.content)
            else:
                print(f"Ошибка при загрузке (код {resp.status_code}): {url}")
        except requests.exceptions.RequestException as e:
            print(f"Исключение при скачивании {url}: {e}")


if __name__ == "__main__":
    # Парсер работает с использованием браузера Firefox и geckodriver.exe

    GECKODRIVER_PATH = "C:/Users/ivana/MLInnopolis/Module2/Lesson32/geckodriver.exe"
    BASE_URL = "https://yandex.ru/images/search"

    DATASET_FOLDER = "C:/Users/ivana/MLInnopolis/Module2/Lesson32/dataset/"
    QUERY = "ship"
    LIMIT = 3000

    # Создаём папку для итоговых изображений
    create_folder_if_not_exists(DATASET_FOLDER)

    print(f"Собираем миниатюры для: {QUERY} ...")
    thumbnail_urls = get_thumbnail_urls(
        query=QUERY,
        limit=LIMIT,
        delay=5,
        headless=False,
        geckodriver_path=GECKODRIVER_PATH,
        base_url=BASE_URL,
    )
    print(f"Найдено миниатюр: {len(thumbnail_urls)}")

    target_path = os.path.join(DATASET_FOLDER, QUERY.replace(" ", "_"))
    download_images(thumbnail_urls, target_path)

    print(f"Готово! Изображения сохранены в папке {target_path}")
