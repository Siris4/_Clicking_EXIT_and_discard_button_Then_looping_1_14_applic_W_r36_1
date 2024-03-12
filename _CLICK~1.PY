from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime

# credentials and paths (ensure these are correctly set)
linkedin_dictionary = {
    "email": "YOUROWNEMAIL",
    "linkedin_password": "YOUROWNPASSWORD",
}


# function to get the current timestamp
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# setup webdriver
def setup_chrome_driver_for_selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()),
                              options=chrome_options)
    return driver


# login to linkedin
def login_to_linkedin(driver):
    driver.get("https://www.linkedin.com/login")
    driver.find_element(By.ID, "username").send_keys(linkedin_dictionary["email"])
    driver.find_element(By.ID, "password").send_keys(linkedin_dictionary["linkedin_password"] + Keys.ENTER)
    print(f"{get_timestamp()}: Successfully logged in to LinkedIn.")


# navigate and apply to jobs
def apply_to_jobs(driver):
    driver.get("https://www.linkedin.com/jobs/search/?keywords=python")
    listings = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable")))
    for index, listing in enumerate(listings):
        # scroll and click on the job listing
        driver.execute_script("arguments[0].scrollIntoView(true);", listing)
        listing.click()
        print(f"{get_timestamp()}: Clicked on job listing {index + 1}.")
        time.sleep(2)

        # click the apply button if available
        try:
            apply_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-apply-button")))
            apply_button.click()
            print(f"{get_timestamp()}: Clicked the apply button for job {index + 1}.")

            # attempt to detect and interact with application form elements
            phone_field = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='phoneNumber']")))
            phone_field.clear()
            phone_field.send_keys(linkedin_dictionary["phone_number"])
            submit_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-control-name='submit_unify']")))
            submit_button.click()
            print(f"{get_timestamp()}: Submitted application for job {index + 1}.")

            # close any modal if open
            close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Dismiss']")))
            close_button.click()

        except TimeoutException:

            print(f"{get_timestamp()}: Attempting to close job application and move to next.")

            try:
                # Generalize the exit button click with common attributes
                exit_buttons = driver.find_elements(By.CSS_SELECTOR,
                                                    "button[aria-label='Dismiss'], button[aria-label='Close'], svg[aria-hidden='true']")
                for button in exit_buttons:
                    if button.is_displayed():
                        button.click()
                        print(f"{get_timestamp()}: Clicked on a general exit button.")
                        break

                # Your added snippet to click on the "Discard" button starts here
                try:
                    # Find all buttons with the class 'artdeco-button__text'
                    potential_discard_buttons = driver.find_elements(By.CSS_SELECTOR,
                                                                     "button > span.artdeco-button__text")
                    # Iterate through the found buttons to click the one with the text 'Discard'
                    for button in potential_discard_buttons:
                        if "Discard" in button.text:
                            # Click the parent button of the span since the span is not clickable
                            parent_button = button.find_element(By.XPATH, "..")
                            parent_button.click()
                            print(f"{get_timestamp()}: Clicked on the 'Discard' button.")
                            break
                except Exception as e:
                    print(f"{get_timestamp()}: Error while trying to click on the 'Discard' button: {e}")
                # Your added snippet ends here

            except Exception as e:
                print(f"{get_timestamp()}: Error during job application cleanup: {e}")

            time.sleep(1)  # adjust sleep time as needed

driver = setup_chrome_driver_for_selenium()
login_to_linkedin(driver)
apply_to_jobs(driver)


# driver.quit()
