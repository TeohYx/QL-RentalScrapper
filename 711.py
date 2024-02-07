import sys
import cloudscraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup, SoupStrainer
import time
import pandas as pd
import os

def connect(url):
    driver = webdriver.Chrome()
    driver.get(url)
    # lists = EC.presence_of_element_located((By.XPATH, '//h3[@class="listing-name"]'))
    # print(driver)
    try:
        elements = WebDriverWait(driver, 10).until(
            # To check if the page loaded successfully
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.uVccjd.HzV7m-pbTTYe-KoToPc-ornU0b-hFsbo.HzV7m-KoToPc-hFsbo-ornU0b")) 
        )
        print("Connection established")
        return elements, driver

    except Exception as e:
        print(f"An error occured: {e}")

def get_stores(contents, driver):
    name_coor = {"Name": [], "Coordinate": []}
    # print(content.find_element(By.CLASS_NAME, "HzV7m-pbTTYe-ibnC6b pbTTYe-ibnC6b-d6wfac"))
    for index, content in enumerate(contents):
        content.click()
    try:
        specific_locations = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.HzV7m-pbTTYe-ibnC6b-V67aGc")))

        for i, specific_location in enumerate(specific_locations):
            # specific_location = WebDriverWait(content, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.HzV7m-pbTTYe-ibnC6b-V67aGc")))
            specific_location.click()
            # driver.implicitly_wait(3)
            try:
                name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div[1]/div[2]')))
                if name.text[0] == "#":
                    print("1")
                    coordinate = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div[4]/div[2]')))
                else:
                    print("2")
                    coordinate = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div[2]/div[2]')))

                print(f"Progress: {i+1} of {len(specific_locations)}")

                name_coor["Name"].extend([name.text])
                name_coor["Coordinate"].extend([coordinate.text])
                # time.sleep(10)
                try:
                    back = WebDriverWait(content, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[3]/div[1]/div/span/span/span')))
                    back.click()
                except:
                    print("Back no found")
                    break

            except Exception as e:
                print(e)          
    except Exception as e:
        print(f"The element is not found when clicked, error: {e}")

    return name_coor
    
    print("end")

def store_excel(name_coor):
    print(name_coor)
    curr_dir = os.getcwd()
    file_name = '7-11 Coordinates.csv'
    output = os.path.join(curr_dir, file_name)
    df = pd.DataFrame.from_dict(name_coor)
    # with open(output, 'a') as f:
    #     df.to_csv(f,header=f.tell()==0, index=False, mode='a')


    df.to_csv(output, index=False)
    print(f"File saved into {output}")

if __name__ == '__main__':
    content, driver = connect("https://www.google.com/maps/d/u/0/viewer?mid=1Dcxo7WR64emFqXx_aivDDMVcdH8")
    print(content)
    if content:
        name_coor = get_stores(content, driver)
    store_excel(name_coor)