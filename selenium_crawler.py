from selenium import webdriver  # 用来驱动浏览器的
from selenium.webdriver import ActionChains  # 破解滑动验证码的时候用的 可以拖动图片
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC  # 和下面WebDriverWait一起用的
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
import time

def crawl():
    driver = webdriver.Chrome()
    data = []

    max_retries = 5

    # driver.get('https://popl18.sigplan.org/track/POPL-2018-papers#event-overview')
    driver.get('https://pldi18.sigplan.org/track/pldi-2018-papers#event-overview')
    time.sleep(5)

    try:
        papers = driver.find_elements(by='xpath', value='//div[@id="event-overview"]//tr//a[@data-event-modal]')
        for i, paper in enumerate(papers):
            print("{}/{}".format(i, len(papers)))
            driver.execute_script("arguments[0].scrollIntoView()", paper)
            time.sleep(0.1 + (i == 0))
            paper.click()

            retry = max_retries
            while retry > 0:
                retry -= 1
                time.sleep(0.2)
                try:
                    title = driver.find_elements(by='xpath', value='//div[@class="bg-primary event-title"]')[-1].text
                    body = driver.find_elements(by='xpath', value='//div[@class="bg-info event-description"]')[-1].get_attribute('outerHTML')
                    if title != '':
                        break
                except:
                    pass
            else:
                title = "Out of retries!"
                body = ""

            data.append((title, body))
            print(data[-1][0])

            driver.find_element(by='link text', value='Close').click()
            driver.implicitly_wait(30)
    except Exception as e:
        print(e)
        input()
    finally:
        driver.close()

    print(len(data))
    print(data)


if __name__ == "__main__":
    crawl()
