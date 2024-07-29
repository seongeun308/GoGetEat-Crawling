import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def create_chrome_driver():
    # ChromeDriver 저장 경로
    chrome_driver_path = os.path.join(os.getcwd(), 'chromedriver')
    print(chrome_driver_path)
    
    # ChromeDriver가 존재하는지 확인
    if not os.path.exists(chrome_driver_path):
        chrome_driver_path = ChromeDriverManager().install()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # ChromeDriver 서비스 생성
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
