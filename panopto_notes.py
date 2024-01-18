# IMPORTS FOR WEBSCRAPING AND OPENAI W/ PIP INSTALLS JUST IN CASE
import os
import time
from datetime import datetime
import sys
required_packages = ["requests", "fake_useragent","selenium", "webdriver_manager", "csv", "openai", "pyautogui"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        os.system(f"pip install {package}")

        os.system(f"pip install {package}")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import pyautogui

def ok_cookies(driver):
    # find cookie button by XPATH and press it
    ok_cookies_button = driver.find_element(By.XPATH, '//*[@id="agree_button"]')
    ok_cookies_button.click()
    return None

def SSO(driver):
    SSO_element = driver.find_element(By.XPATH, '//*[@id="login-link"]')
    href = SSO_element.get_attribute("href")
    driver.get(href)
    time.sleep(3)
    # driver.find_element(By.TAG_NAME,'body').send_keys('rcdoug03@louisville.edu')
    pyautogui.typewrite("rcdoug03@louisville.edu")
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.TAB)
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.TAB)
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.TAB)
    # driver.find_element(By.TAG_NAME,'body').send_keys(Keys.TAB)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.typewrite("sSTtBzt%&hS6ELwjJ2uT")
    # driver.find_element(By.TAG_NAME,'body').send_keys(Keys.TAB)
    # driver.find_element(By.TAG_NAME,'body').send_keys(Keys.TAB)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(4)
    pyautogui.press('enter')

# get transcript title
def get_title(driver):
    
    title = ''
    # find the details tab and select
    print('finding details tab')
    try:
        details_tab = driver.find_element(By.XPATH, '//*[@id="detailsTabHeader"]')
        print("\tcomplete")
    except Exception as e:
        return None
    print('selecting details tab')
    try:
        driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", details_tab, 'aria-selected', "true")
        print("\tcomplete")
    except Exception as e:
        return None
    print('finding details pane')
    try:
        details_pane = driver.find_element(By.XPATH,'//*[@id="detailsTabPane"]')
        print("\tcomplete")
    except Exception as e:
        return None
    print('grabbing lecture name')
    try:
        name = details_pane.find_element(By.CLASS_NAME, 'name')
        inner_html = name.get_attribute("innerHTML")
        title += inner_html
        print("\tcomplete")
    except Exception as e:
        return None
    return title

# Select the "captions" tab
def captions(driver):
    # Find captions tab and select
    print("find/select caption tab")
    try:
        captions_tab = driver.find_element(By.XPATH, '//*[@id="transcriptTabHeader"]')
        driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", captions_tab, 'aria-selected', "true")
        print("\tcomplete")
    except Exception as e:
        print(e)

# Find the transcript on the Panopto content
def find_transcript(driver, title):
    # Navigate to panopto recording. might not need to...
    # driver.get(url)

    # empty string to fill with transcript
    transcript = f"{title}\n"
    print("finding transcript elements and compiling list")
    try:
        transcript_list = driver.find_element(By.XPATH, '//*[@id="transcriptTabPane"]/div[3]/ul')
        text_elements = transcript_list.find_elements(By.CLASS_NAME, 'event-text')
        print("\tcomplete")
    except Exception as e:
        print(e)

    for text in text_elements:
        try:
            span = text.find_element(By.TAG_NAME, 'span')
            inner_html = span.get_attribute("innerHTML")
            transcript += f"{inner_html} "
        except Exception as e:
            print(f"{e}\n\tfor {text}")
    return transcript

# formatting
def format_transcript(transcript):
    translist = transcript.split(".")
    transcript = ".\n".join(translist)
    return transcript


if __name__ == "__main__":
    start = datetime.now()
    url = sys.argv[1]
    ua = UserAgent()
    user_agent = ua.random
    options = Options()
    # options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)
    panopto = "https://louisville.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=1753ae0d-512a-41d9-b354-b0f1013923ae"
    driver.get(url)
    time.sleep(3)
    if "action=relogin" in driver.current_url:
        ok_cookies(driver)
        time.sleep(1)
        SSO(driver)
    else:
        print("something went wrong trying to navigate to login")
        exit()
    time.sleep(5)
    title = None
    while title == None:
        title = get_title(driver)
        print("Trying to get the title again...")
        time.sleep(2)
    captions(driver)
    time.sleep(1)
    transcript = find_transcript(driver, title)
    transcript = format_transcript(transcript)
    print(transcript)
    print("writing text to file:")
    with open(f"{title}.txt", 'w', encoding='utf-8') as f:
        f.write(transcript)
        f.close()
    print(f"Written to: {title}.txt")
    print(f"RUNTIME: {datetime.now() - start}")
    time.sleep(10)
