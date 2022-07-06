import pyautogui
import random
import time
import string
from alright import WhatsApp
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def sessionGenerator():
    messager = WhatsApp()
    sent = 0
    unsent = 0
    numbers = [
        8861562478,
        9242137092,
        9110208429,
        8861562478,
        9242137092,
        9110208429,
        8861562478,
        9242137092,
        9110208429,
        8861562478,
        9242137092,
        9110208429,
        8861562478,
        9242137092,
        9110208429,
        8861562478,
        9242137092,
        9110208429,
        8861562478,
        9242137092,
        9110208429,
        8861562478,
        9242137092,
        9110208429,
        8861562478,
        9242137092,
        9110208429,
        8861562478,
        9242137092,
    ]

    message = "(Jenkins Server Message)This is a test message for testing purpose, please ignore"
    x_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'

    # browser = webdriver.Chrome(ChromeDriverManager().install())
    # browser.get("https://web.whatsapp.com/")
    print("************** Waiting for QR code scan ***********")
    # time.sleep(5)
    print('generating screen shot name...')
    res = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=8))
    if messager.QR_screen_shot(res):
        print('screen shot recieved')
    else:
        print('screenshot not receieved')

    time.sleep(15)
    for number in numbers:
        user_num = '91' + str(int(number))
        messager.find_user(user_num)
        try:
            browser = messager.get_browser_instance()
            input_box = WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.XPATH, x_path)))

            input_box.send_keys(message, Keys.ENTER)
            time.sleep(5)
            sent += 1
            print(f"Message sent successfuly to "+user_num)
            # result = messager.send_message(message, x_path)
            # if not result:
            #     print("message sending failed for "+user_num)
            #     # not_sent_list.append(str(number))
            # else:
            #    print('message sent')

        except Exception as e:
            # print(e)
            print("message sending failed for "+user_num)
            unsent += 0
    # res = ''.join(random.choices(
    #     string.ascii_uppercase + string.digits, k=8))
    # QR_CODE = browser.find_element(
    #     by=By.XPATH, value='//*[@id="app"]/div/div/div[2]/div[1]')
    # time.sleep(3)
    # QR_CODE.screenshot('qr_codes_wtsapp/'+res + '.png')
    # _wait_for_presence_of_an_element(browser, MAIN_SEARCH_BAR__SEARCH_ICON)
    # session = browser.execute_script(EXTRACT_SESSION)
    # with open(sessionFilePath, "w", encoding="utf-8") as sessionFile:
    #     sessionFile.write(str(session))

    # print("Your session file is saved to: " + sessionFilePath)
    print('-------Report----------')
    print('Total Numbers: '+str(len(numbers)))
    print('Sent Numbers: '+str(sent))
    print('Unsent Numbers: '+str(unsent))
    # print(session)
    time.sleep(160)
    # browser.close()


sessionGenerator()
