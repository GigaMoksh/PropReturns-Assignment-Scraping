from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import pytesseract
import csv
from googletrans import Translator
from typing import List


translator = Translator()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.get("https://freesearchigrservice.maharashtra.gov.in/")


def scrape() -> List[List]:
    close = driver.find_element(By.XPATH, '//*[@id="popup"]/div/a')
    close.click()
    # Close the "close" button which appears when we open the website

    district_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="ddlDistrict"]'))
    district_dropdown.select_by_value("31")
    # select the mumbai upnagar as the district

    action = ActionChains(driver)
    source = driver.find_element(By.XPATH, '//*[@id="txtAttributeValue"]')
    action.move_to_element(source).click().perform()
    # Move your mouse to the property no

    time.sleep(40)

    village_name = driver.find_element(By.XPATH, '//*[@id="txtAreaName"]')
    village_name.send_keys("Andheri")
    # Type Andheri in the village name textbox

    action = ActionChains(driver)
    source = driver.find_element(By.XPATH, '//*[@id="txtAttributeValue"]')
    action.move_to_element(source).click().perform()
    # Move your mouse to the property no

    time.sleep(45)

    village_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="ddlareaname"]'))
    village_dropdown.select_by_value("Andheri")
    # Select the village as andheri in the dropdown menu

    property_no = driver.find_element(By.XPATH, '//*[@id="txtAttributeValue"]')
    property_no.send_keys("13")
    # Type 13 in the property number textbox

    driver.find_element(By.XPATH, '//*[@id="imgCaptcha"]').screenshot("./image.png")
    image = Image.open("./image.png")
    # Save the captcha image as a png and open it using PIL library

    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    )
    text = (pytesseract.image_to_string(image)) + "\n\n\n\n"
    captcha_box = driver.find_element(By.XPATH, '//*[@id="txtImg"]')
    captcha_box.send_keys(text)
    # Extract the text from the captcha image using pytesseract and use it in the captcha box

    search_button = driver.find_element(By.XPATH, '//*[@id="btnSearch"]')
    search_button.click()
    # Click on the search button

    time.sleep(80)

    driver.find_element(By.XPATH, '//*[@id="imgCaptcha"]').screenshot("./image.png")
    image = Image.open("./image.png")
    # Save the captcha image as a png and open it using PIL library

    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    )
    text = (pytesseract.image_to_string(image)) + "\n\n\n\n"
    captcha_box = driver.find_element(By.XPATH, '//*[@id="txtImg"]')
    captcha_box.send_keys(text)
    # Extract the text from the captcha image using pytesseract and use it in the captcha box

    search_button = driver.find_element(By.XPATH, '//*[@id="btnSearch"]')
    search_button.click()
    # Click on the search button

    time.sleep(180)

    data = []
    for k in range(1, 16):
        for i in range(2, 12):
            xpath = f'//*[@id="RegistrationGrid"]/tbody/tr[{i}]'
            doc_no = driver.find_element(By.XPATH, f"{xpath}/td[1]").text
            dname = driver.find_element(By.XPATH, f"{xpath}/td[2]").text
            rdate = driver.find_element(By.XPATH, f"{xpath}/td[3]").text
            sro_name = driver.find_element(By.XPATH, f"{xpath}/td[4]").text
            seller_name = driver.find_element(By.XPATH, f"{xpath}/td[5]").text
            purchaser_name = driver.find_element(By.XPATH, f"{xpath}/td[6]").text
            property_desc = driver.find_element(By.XPATH, f"{xpath}/td[7]").text
            sro_code = driver.find_element(By.XPATH, f"{xpath}/td[8]").text
            status = driver.find_element(By.XPATH, f"{xpath}/td[9]").text

            data.append(
                [
                    doc_no,
                    dname,
                    rdate,
                    sro_name,
                    seller_name,
                    purchaser_name,
                    property_desc,
                    sro_code,
                    status,
                ]
            )
        if k == 15:
            break
        next_page = driver.find_element(
            By.XPATH,
            f'//*[@id="RegistrationGrid"]/tbody/tr[12]/td/table/tbody/tr/td[{k + 1}]',
        )
        next_page.click()
        time.sleep(70)

    return data


def main() -> None:
    data = scrape()
    with open(
        "data1.csv",
        "w",
        encoding="utf-8",
    ) as f:
        csv_writer = csv.writer(f, delimiter=":")
        csv_writer.writerow(
            [
                "doc_no",
                "dname",
                "rdate",
                "sro_name",
                "seller_name",
                "purchaser_name",
                "property_desc",
                "sro_code",
                "status",
            ]
        )
        csv_writer.writerows(data)


if __name__ == "__main__":
    main()
