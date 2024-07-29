from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dto import MenuInfoDto
import config

def get_kakaoMap_menu(driver, url):
    driver.get(url)
    driver.implicitly_wait(5)
    
    try:
        config.logging.info(f'--------------- start crawling {url}')

        # 현재 메뉴 목록 크기 확인
        menu_items = driver.find_elements(By.CSS_SELECTOR, "#mArticle > div.cont_menu > ul > li")  # 메뉴 항목의 CSS Selector
        current_menu_count = len(menu_items)
        
        # "메뉴 더보기" 버튼이 있는지 확인
        more_button_present = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.link_more[data-logevent='additional_info,menu,more_menu']"))
        )
        
        if more_button_present:
            while True:
                try:
                    # "메뉴 더보기" 버튼이 클릭 가능할 때까지 대기
                    more_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.link_more[data-logevent='additional_info,menu,more_menu']"))
                    )
                    more_button.click()
                    
                    # 메뉴 항목이 추가될 때까지 대기
                    WebDriverWait(driver, 5).until(
                        lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "#mArticle > div.cont_menu > ul > li")) > current_menu_count
                    )
                    current_menu_count = len(driver.find_elements(By.CSS_SELECTOR, "#mArticle > div.cont_menu > ul > li"))
                    
                    # "메뉴 접기" 버튼이 나타나는지 확인
                    close_button = driver.find_element(By.CSS_SELECTOR, "a.link_more.link_close[data-logevent='additional_info,menu,more_menu']")
                    if close_button.is_displayed():
                        break
                except Exception as e:
                    config.logging.info(f"Error clicking the link or loading dynamic content: {e}")
                    break
    except Exception as e:
        config.logging.info(f"No 'more menu' button found or error occurred: {e}")
    
    # 페이지 소스 가져오기
    html = driver.page_source
    
    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(html, 'html.parser')
    
    # 모든 메뉴 이름을 추출
    menus = []
    menu_elements = soup.find_all('span', class_='loss_word')
    for element in menu_elements:
        menus.append(element.text)
    
    config.logging.info(f'--------------- end crawling {url}')
    
    return MenuInfoDto(store_url=url, menu_list=menus)

