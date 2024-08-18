from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
from dotenv import load_dotenv
import time

load_dotenv()

# -------------------------- CONSTANTS --------------------------#

PROMISED_DOWN = 25
PROMISED_UP = 25
X_EMAIL = os.getenv("X_EMAIL")
X_PASSWORD = os.getenv("X_PASSWORD")
X_USERNAME = os.getenv("X_USERNAME")
INTERNET_PROVIDER =  os.getenv("INTERNET_PROVIDER")


# ---------------------------- BODY ----------------------------#

class InternetSpeedTwitterBot:
    SPEEDTEST_URL = "https://www.speedtest.net"
    X_URL = "https://www.x.com"

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.implicitly_wait(1)

        self.up = 0
        self.down = 0

        # self.up_speed, self.down_speed = 50, 50  # debugger
        self.down_speed, self.up_speed = self.get_internet_speed()

    def get_internet_speed(self):
        self.driver.get(self.SPEEDTEST_URL)

        start_button = self.driver.find_element(By.CSS_SELECTOR, ".start-text")
        start_button.click()

        time.sleep(30)

        # Grab the new values
        self.down = self.driver.find_element(
            By.CSS_SELECTOR,
            ".result-data-large.number.result-data-value.download-speed")
        self.up = self.driver.find_element(By.CSS_SELECTOR, ".result-data-large.number.result-data-value.upload-speed")

        # While the up text has not yet come out
        while self.up.text == "—":
            self.down = self.driver.find_element(  # Once up text is --, down is done testing. Store value
                By.CSS_SELECTOR,
                ".result-data-large.number.result-data-value.download-speed")
            time.sleep(1)  # Keep pausing the next line of code for 1 second until it's done

        print(self.down.text)
        print(self.up.text)
        return float(self.down.text), float(self.up.text)

    def log_in_twitter(self):
        self.driver.get(self.X_URL)
        wait = WebDriverWait(self.driver, 105)  # Wait up to 15 seconds

        time.sleep(3)

        try:
            x_sign_in = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                               '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[3]/a/div/span')))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", x_sign_in)  # Scroll into view
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", x_sign_in)  # Use JS to click because can't access o therwise
            time.sleep(1)
            x_sign_in.click()
        except Exception as e:
            print(f"Failed to click sign in: {e}")

        # TODO Enter Email
        try:
            email = wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')))
            time.sleep(1)
            email.send_keys(X_EMAIL, Keys.ENTER)
        except Exception as e:
            print(f"Failed to type email: {e}")

        # TODO Enter Username if prompted -- THIS DOESN'T WORK! :(
        try:
            username = wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')))
            time.sleep(1)
            username.send_keys(X_USERNAME, Keys.ENTER)
        except Exception as e:
            print(f"Failed to type email: {e}")

        # TODO Enter Password
        try:
            password = wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')))
            time.sleep(1)
            password.send_keys(X_PASSWORD, Keys.ENTER)
        except Exception as e:
            print(f"Failed to type password: {e}")

        # TODO Click close 2FA if it asks for this
        try:
            close_2fa = wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/button')))
            time.sleep(1)
            close_2fa.click()
        except Exception as e:
            print(f"Failed to click on the close 2FA button: {e}")

        time.sleep(2)

    def tweet_at_provider(self):
        wait = WebDriverWait(self.driver, 10)  # Wait up to 10 seconds

        # TODO Set up the message
        if self.up_speed < 37 or self.down_speed < 37:
            tweet = (
                f"Hey @{INTERNET_PROVIDER}, why is my internet speed {self.down_speed} Mpbs down/{self.up_speed} Mpbs up when I pay for \""
                f"{PROMISED_DOWN} Mpbs down/{PROMISED_UP} Mbps up?")
        else:
            tweet = (f"Hey @{INTERNET_PROVIDER}, good job! My internet speed is {self.down_speed} Mbps down/{self.up_speed} Mbps up against \""
                     f"the promised speed of {PROMISED_DOWN} Mbps down/{PROMISED_UP} Mbps up!")


        # TODO Compose the tweet
        try:
            compose_tweet = wait.until(
                EC.element_to_be_clickable(((By.XPATH,
                                             '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div')))
            )
            time.sleep(1)
            compose_tweet.send_keys(tweet)
        except Exception as e:
            print(f"Failed to click on the close 2FA button: {e}")


        # TODO Click Post! :D
        try:
            send_tweet = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button')))
            time.sleep(1)
            send_tweet.click()
        except Exception as e:
            print(f"Failed to click on the close 2FA button: {e}")


internet_speed_bot = InternetSpeedTwitterBot()
internet_speed_bot.log_in_twitter()
internet_speed_bot.tweet_at_provider()
