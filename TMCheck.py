from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Reading names from input.txt
with open("input.txt", "r") as file:
    names = [line.strip() for line in file]

# Setting up Chrome WebDriver
chrome_service = Service('./chromedriver-win64/chromedriver.exe')
chrome_service.start()
driver = webdriver.Chrome(service=chrome_service)

# Opening webpage
driver.get("https://tmrsearch.ipindia.gov.in/tmrpublicsearch/")

# Loop through each name
for name in names:
    # Find and set dropdown value to "Contains"
    dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_DDLFilter"))
    dropdown.select_by_value("1")

    # Insert name in lowercase into input box
    wordmark_input = driver.find_element(By.ID, "ContentPlaceHolder1_TBWordmark")
    wordmark_input.clear()
    wordmark_input.send_keys(name.lower())

    # Insert value "41" into class input box
    class_input = driver.find_element(By.ID, "ContentPlaceHolder1_TBClass")
    class_input.clear()
    class_input.send_keys("41")

    # Print instructions and input Captcha from the user
    captcha = input("Enter Captcha: ")

    # Insert Captcha into text field
    captcha_input = driver.find_element(By.ID, "ContentPlaceHolder1_captcha1")
    captcha_input.clear()
    captcha_input.send_keys(captcha)

    # Click on Search button
    search_button = driver.find_element(By.ID, "ContentPlaceHolder1_BtnSearch")
    search_button.click()

    # Wait for the new page to load
    WebDriverWait(driver, 120).until(EC.url_contains("https://tmrsearch.ipindia.gov.in/tmrpublicsearch/tmsearch.aspx"))

    # Check if No Record found in table 1
    table1 = driver.find_element(By.ID, "ContentPlaceHolder1_GVINP")
    if "No Record found" in table1.text:
        status1 = "available"
    else:
        status1 = "unavailable"

    # Check if No Record found in table 2
    table2 = driver.find_element(By.ID, "ContentPlaceHolder1_MGVSearchResult")
    if "No Record found" in table2.text:
        status2 = "unregistered"
    else:
        status2 = "registered"

    print(f"Name: {name}, Status 1: {status1}, Status 2: {status2}")

    # Click on Next button
    next_button = driver.find_element(By.ID, "ContentPlaceHolder1_LnkNextSearch")
    next_button.click()

# Quit WebDriver
driver.quit()
