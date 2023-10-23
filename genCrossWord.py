from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
import time
import json
from selenium.webdriver.chrome.options import Options


def click_element(driver, xPath):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xPath)))


def main():
    print("Running...")
    with open("./titleClue.json") as f:
        data = json.load(f)

    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    # driver.implicitly_wait(10)

    # driver.get("http://localhost:4002/crossword-puzzle-maker")
    driver.get('https://worksheetzone.org/crossword-puzzle-maker')

    # Login
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]/div[3]/div/div/div/div/div/div'))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div'))).click()

    for i in range(10):
        driver.find_element(
            By.XPATH, '/html/body/div[3]/div[3]/div/div/div[4]/div[1]').click()

    driver.switch_to.alert.accept()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]/div[3]/div/div/div/div/div/div'))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div'))).click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id=":r7:"]'))).send_keys('worksheetzone.ad@gmail.com', Keys.ENTER)

    time.sleep(5)

    for el in data:
        topic = el["topic"]
        print("Current topic: ", topic)
        ws_count = 0
        for topic_data in el["data"]:
            driver.implicitly_wait(0)
            title = topic_data["title"]
            list_words = topic_data["words"]
            long_words_count = 0
            ws_count += 1

            # if (topic_data["status"] == "oke"):
            #     pass

            print('Current ws title: ', title)
            try:
                driver.refresh()

                actions = ActionChains(driver)
                title_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#content-layer > div > div > div > div:nth-child(2)')))
                actions.double_click(title_element).perform()
                actions.send_keys(title).perform()

                # leave title field
                ActionChains(driver).move_to_element_with_offset(
                    title_element, 100, 100).click().perform()

                # Random layout
                random_index = random.choice([0, 1, 2, 3, 4, 5])
                if random_index != 0:
                    layout_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="CROSSWORD"]/div[2]/div/div[2]/div[1]/div[2]/div')))
                    layout_tab.click()
                    options = driver.find_elements(
                        By.XPATH, '//*[@id=":r5:"]/li')
                    option = options[random_index]
                    driver.execute_script(
                        "arguments[0].scrollIntoView(true);", option)
                    option.click()

                if random.choice([0, 1]):
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="CROSSWORD"]/div[2]/div/div[2]/div[2]/div/div[1]/span'))).click()

                # Switch input tab and fill input
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="CROSSWORD"]/div[2]/div/div[1]/div[3]/div[1]/button[2]'))).click()

                input_field = driver.find_element(
                    By.XPATH, '//*[@id="multi-text"]')
                for word in list_words:
                    if len(word["value"]) > 12:
                        long_words_count += 1

                    if long_words_count > 2 and len(word["value"]) > 12:
                        continue

                    line = f'{word["value"]},{word["clue"]}\n'
                    input_field.send_keys(line)

                    if ws_count <= 20:
                        try:
                            driver.find_element(
                                By.XPATH, '//*[@id="page-worksheet_1"]')
                            isNewPage = True
                        except Exception:
                            isNewPage = False

                        if isNewPage:
                            # Clear last word
                            if len(line) < 43:
                                ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ARROW_LEFT).send_keys(
                                    Keys.ARROW_UP + Keys.BACK_SPACE).key_up(Keys.SHIFT).perform()
                            else:
                                ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ARROW_LEFT).send_keys(
                                    Keys.ARROW_UP + Keys.ARROW_UP + Keys.BACK_SPACE).key_up(Keys.SHIFT).perform()

                            for i in range(5):
                                driver.find_element(
                                    By.XPATH, '//*[@id="CROSSWORD"]/div[2]/div/div[2]/div[2]/button').click()
                                try:
                                    driver.find_element(
                                        By.XPATH, '//*[@id="page-worksheet_1"]')
                                except Exception:
                                    break
                            break

                # Save
                driver.implicitly_wait(10)
                driver.find_element(
                    By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]/div[1]').click()

                title_field = driver.find_element(
                    By.CSS_SELECTOR, 'div.title-worksheet > input')
                title_field.send_keys(title + Keys.ENTER)
                time.sleep(1)

                des = driver.find_element(
                    By.XPATH, '//*[@id="description-textarea"]')
                des.send_keys('Test'+Keys.ENTER)
                time.sleep(1)

                language = driver.find_element(
                    By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div[3]/div[1]/div[2]/div[2]/div/input')
                language.send_keys("English" + Keys.ARROW_DOWN + Keys.ENTER)
                time.sleep(1)

                grade = driver.find_element(
                    By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div[3]/div[1]/div[2]/div[3]/div/input')
                grade.send_keys("Grade 1" + Keys.ARROW_DOWN + Keys.ENTER)
                grade.send_keys("Grade 2" + Keys.ARROW_DOWN + Keys.ENTER)
                grade.send_keys("Grade 3" + Keys.ARROW_DOWN + Keys.ENTER)
                time.sleep(1)

                tag = driver.find_element(
                    By.XPATH, "/html/body/div[3]/div[3]/div/div/div/div/div[3]/div[1]/div[2]/div[4]/div/input")
                tag.send_keys(topic + Keys.ENTER)
                time.sleep(1)

                topic_data["status"] = "oke"
                with open('./titleClue.json', 'w') as file:
                    json.dump(data, file)

            except Exception as e:
                print(e)
                topic_data["status"] = "failed"
                with open('./titleClue.json', 'w') as file:
                    json.dump(data, file)


if __name__ == "__main__":
    main()
