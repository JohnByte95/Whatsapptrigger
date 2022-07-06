"""
Alright is unofficial Python wrapper for whatsapp web made as an inspiration from PyWhatsApp
allowing you to send messages, images, video and documents programmatically using Python
"""


import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    UnexpectedAlertPresentException,
    NoSuchElementException,
)
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW


import requests


class WhatsApp(object):
    def __init__(self, browser=None):
        self.BASE_URL = 'https://web.whatsapp.com/send?phone='
        self.suffix_link = 'https://wa.me/'

        if not browser:
            browser = webdriver.Chrome(
                ChromeDriverManager().install(),
                options=self.chrome_options,
            )
            # # Service Object that manages the starting and stopping of the ChromeDriver
            # # Creates a new instance of the Service
            # service = Service(ChromeDriverManager().install())
            # service.creationflags = CREATE_NO_WINDOW
            # browser = webdriver.Chrome(
            #     service=service,
            #     options=self.chrome_options,
            # )

        self.browser = browser

        self.wait = WebDriverWait(self.browser, 600)
        self.wait_user = WebDriverWait(self.browser, 15)
        self.login()
        self.mobile = ''

    @property
    def chrome_options(self):
        chrome_options = Options()
        if sys.platform == "win32":
            chrome_options.add_argument('--profile-directory=Default')
            chrome_options.add_argument(
                '--user-data-dir=C:/Temp/ChromeProfile')
        else:
            chrome_options.add_argument("start-maximized")
            chrome_options.add_argument('--user-data-dir=./User_Data')
        return chrome_options

    def login(self):
        self.browser.get(self.BASE_URL)
        self.browser.minimize_window()

    def get_phone_link(self, mobile) -> str:
        """get_phone_link (), create a link based on whatsapp (wa.me) api

        Args:
            mobile ([type]): [description]

        Returns:
            str: [description]
        """
        return f'{self.BASE_URL}{mobile}'

    def catch_alert(self, seconds=3):
        """catch_alert()

            catches any sudden alert
        """
        try:
            WebDriverWait(self.browser, seconds).until(EC.alert_is_present())
            alert = self.browser.switch_to_alert.accept()
            return True
        except Exception as e:
            print(e)
            return False

    def find_user(self, mobile) -> None:
        """find_user()
        Makes a user with a given mobile a current target for the wrapper

        Args:
            mobile ([type]): [description]
        """
        try:
            self.mobile = mobile
            link = self.get_phone_link(mobile)
            self.browser.get(link)

        except UnexpectedAlertPresentException as bug:
            print(bug)
            time.sleep(1)
            self.find_user(mobile)

    def find_by_username(self, username):
        """find_user_by_name ()

        locate existing contact by username or number

        Args:
            username ([type]): [description]
        """
        try:
            search_box = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
            search_box.clear()
            search_box.send_keys(username)
            search_box.send_keys(Keys.ENTER)
        except Exception as bug:
            error = f'Exception raised while finding user {username}\n{bug}'
            print(error)

    def username_exists(self, username):
        """username_exists ()

        Returns True or False whether the contact exists or not, and selects the contact if it exists, by checking if the search performed actually opens a conversation with that contact

        Args:
            username ([type]): [description]
        """
        try:
            search_box = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
            search_box.clear()
            search_box.send_keys(username)
            search_box.send_keys(Keys.ENTER)
            opened_chat = self.browser.find_element_by_xpath(
                "/html/body/div/div[1]/div[1]/div[4]/div[1]/header/div[2]/div[1]/div/span")
            title = opened_chat.get_attribute("title")
            if title.upper() == username.upper():
                return True
            else:
                return False
        except Exception as bug:
            error = f'Exception raised while finding user {username}\n{bug}'
            print(error)

    def is_user_on_WhatsApp(self) -> bool:
        try:
            inp_xpath = '//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]'
            input_box = self.wait_user.until(
                EC.presence_of_element_located((By.XPATH, inp_xpath)))
            return True
        except:
            return False

    def send_message(self, message, x_path):
        """send_message ()
        Sends a message to a target user

        Args:
            message ([type]): [description]
        """
        try:
            inp_xpath = x_path

            # try:
            #     self.browser.implicitly_wait(10)
            # except Exception as e:
            #     print(e)

            input_box = WebDriverWait(self.browser, 15).until(
                EC.presence_of_element_located((By.XPATH, inp_xpath)))

            # input_box = self.wait.until(
            #     EC.presence_of_element_located((By.XPATH, inp_xpath)))
            if len(message) == 2:
                print('single line')
                input_box.send_keys(message[0], Keys.ENTER)
            else:
                print('multy line')
                for line in message:
                    input_box.send_keys(line + Keys.SHIFT + Keys.ENTER)

                input_box.send_keys(Keys.ENTER)

            print(f"Message sent successfuly to {self.mobile}")
            return True
        except (NoSuchElementException, Exception) as bug:

            print(f'Failed to send a message to {self.mobile}')
            return False

    def find_attachment(self):
        clipButton = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="main"]/footer//*[@data-icon="clip"]/..')))
        clipButton.click()

    def send_attachment(self):
        # Waiting for the pending clock icon to disappear
        self.wait.until_not(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"]')))

        sendButton = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div/span')))
        sendButton.click()

    def send_picture(self, picture):
        """send_picture ()

        Sends a picture to a target user

        Args:
            picture ([type]): [description]
        """
        try:
            filename = os.path.realpath(picture)
            self.find_attachment()
            # To send an Image
            imgButton = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/footer//*[@data-icon="attach-image"]/../input')))
            imgButton.send_keys(filename)
            self.send_attachment()
            print(f"Picture has been successfully sent to {self.mobile}")
        except (NoSuchElementException, Exception) as bug:
            print(bug)
            print(f'Failed to send a picture to {self.mobile}')

    def send_video(self, video):
        """send_video ()

        Sends a video to a target user

        Args:
            video ([type]): [description]
        """
        try:
            filename = os.path.realpath(video)
            self.find_attachment()
            # To send a Video
            video_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/footer//*[@data-icon="attach-image"]/../input')))
            video_button.send_keys(filename)
            self.send_attachment()
            print(f'Video has been successfully sent to {self.mobile}')
        except (NoSuchElementException, Exception) as bug:
            print(bug)
            print(f'Failed to send a video to {self.mobile}')

    def send_file(self, filename):
        """send_file()

        Sends a file to target user

        Args:
            filename ([type]): [description]
        """
        try:
            filename = os.path.realpath(filename)
            self.find_attachment()
            document_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/footer//*[@data-icon="attach-document"]/../input')))
            document_button.send_keys(filename)
            self.send_attachment()
        except (NoSuchElementException, Exception) as bug:
            print(bug)
            print(f'Failed to send a PDF to {self.mobile}')

    def is_user_on_WhatsApp(self) -> bool:
        try:
            inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[1]/div/div[2]'
            input_box = self.wait_user.until(
                EC.presence_of_element_located((By.XPATH, inp_xpath)))
            return True
        except:
            return False

    # Testing

    def QR_screen_shot(self, res) -> bool:
        time.sleep(20)
        res = str(time.time()) + res
        try:
            print('Finding QR code')
            QR_CODE = self.browser.find_element(
                by=By.XPATH, value='//*[@id="app"]/div/div/div[2]/div[1]')
            time.sleep(3)
            image = QR_CODE.screenshot('qr_codes_wtsapp/'+res + '.png')

            print('QR code screen shot saved.')

            # sending to numasoftworks server
            image_path = 'qr_codes_wtsapp/'+res + '.png'

            test_file = open(image_path, "rb")
            test_response = requests.post('https://numasoftworks.com/pillzy/api/image', files={"image": test_file})
            print(test_response.json())
            return True
        except:
            return False

    def get_browser_instance(self):
        return self.browser
