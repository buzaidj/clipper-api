import os
import time

if not os.path.exists("./downloads"):
    os.makedirs("./downloads")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse

from parse_clipper_pdf import read_clipper_pdf_to_df


def login_and_retrieve_clipper(email, password):
    """
    NOTE: Right now, this only works for your most recently used card, sometimes
    """
    try:
        options = Options()

        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", "application/pdf"
        )  # Set MIME type for PDF
        # disable the built-in PDF viewer
        options.set_preference("pdfjs.disabled", False)

        driver = webdriver.Firefox(executable_path="./geckodriver", options=options)
        driver.get("https://www.clippercard.com/ClipperWeb/login.html")

        print(driver)

        wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
        wait.until(EC.presence_of_element_located((By.ID, "input-email")))

        email_input = driver.find_element_by_id("input-email")
        password_input = driver.find_element_by_id("input-password")

        email_input.send_keys(email)
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)

        driver.implicitly_wait(3)

        wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "card-" + str(0) + "-dropdown-toggle")
            )
        )

        wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        elem = driver.find_element_by_id("card-" + str(0) + "-dropdown-toggle")
        elem.click()
        time.sleep(1)
        while elem.get_attribute("aria-expanded") == "false":
            elem.click()
            time.sleep(1)

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@data-form-action="/ClipperWeb/view-activity"]')
            )
        )
        view_activity_elements = driver.find_elements_by_xpath(
            '//*[@data-form-action="/ClipperWeb/view-activity"]'
        )

        first_view_activity_elem = view_activity_elements[0]
        first_view_activity_elem.click()
        try:
            first_view_activity_elem.click()
        except:
            pass

        wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
        input_start_date = wait.until(
            EC.presence_of_element_located((By.ID, "input-start-date"))
        )
        # input_start_date = driver.find_element_by_id('input-start-date')
        input_start_date.clear()
        min_date = input_start_date.get_attribute("data-validation-min-date")
        input_start_date.send_keys(min_date)

        download_pdf = driver.find_element_by_css_selector("button.btn.btn-clipper")
        download_pdf.click()

        download_pdf.click()
        driver.implicitly_wait(5)

        # wait for the PDF to download before printing the pdf file location
        time.sleep(3)

        all_handles = driver.window_handles

        df = None
        for handle in all_handles:
            driver.switch_to.window(handle)
            curr_url = driver.current_url
            if "rideHistory" in curr_url:
                print(f"Found saved PDF at {curr_url}")
                df = read_clipper_pdf_to_df(curr_url)
                print(f"Converted PDF to DataFrame")

        # # Switch back to the original tab (if needed)
        # driver.switch_to.window(all_handles[0])

        if df is None:
            raise AssertionError("df should not be none, it should exit")
        return df
    finally:
        _driver = locals().get("driver", None)
        if _driver is not None:
            _driver.quit()


def clipper_df_to_dict(df):
    df = df.reset_index(drop=True)
    return {"records": df.to_dict(orient="records")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", help="Clipper account email address")
    parser.add_argument("--password", help="Clipper account password")
    args = parser.parse_args()

    email = args.email
    password = args.password

    clipper_data = login_and_retrieve_clipper(email, password)

    print(clipper_df_to_dict(clipper_data))

    clipper_data.to_csv("my_output.csv", index=False)
