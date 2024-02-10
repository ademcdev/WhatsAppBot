from time import sleep
import warnings
import win32gui
import win32con
from fuzzywuzzy import fuzz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

warnings.simplefilter("ignore")
url = f'https://web.whatsapp.com/'
chromeDriverPath = 'chromedriver.exe'
chromeOptions = Options()
service = Service(chromeDriverPath)
userAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
chromeOptions.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(service=service, options=chromeOptions)
driver.implicitly_wait(3)
driver.maximize_window()
driver.get(url)
wait = WebDriverWait(driver, 60)
try:
    print('Waiting for the QR scan')
    wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]/div[2]/div/div/div[11]/div/div/div/div[2]/div[1]/div[1]/span')))
    print('QR scanned succesfully')
except TimeoutException:
    print('QR not scanned during the given time')

def clickPerson(targetName):
    contactElements = driver.find_elements(By.CLASS_NAME, '_11JPr')
    
    for contactElement in contactElements:
        userName = contactElement.text.lower().replace(" ", "")
        targetName = targetName.lower().replace(" ", "")
        
        if targetName in userName:
            print(userName)
            contactElement.click()
            sleep(1)
            return True
        else:
            print(f'{targetName} cannot found')
            sleep(10)
    return False

def isOnline():
    try:
        # statusElement = driver.find_element(By.XPATH, '//*[@id="main"]/header/div[2]/div[2]/span')
        # wait.until(ec.staleness_of(statusElement))
        statusElement = driver.find_element(By.XPATH, '//*[@id="main"]/header/div[2]/div[2]/span')
        global status
        status = statusElement.text.lower()
        print(status)
    except StaleElementReferenceException:
        print('Stale Element Reference Exception, trying again...')
        focusApp('whatsapp')
        
def focusApp(appName):
    def callback(handleWindow, extraData):
        windowTitle = win32gui.GetWindowText(handleWindow).lower()
        ratio = fuzz.partial_ratio(appName.lower(), windowTitle)
        if ratio > 80:
            if win32gui.IsIconic(handleWindow):
                win32gui.ShowWindow(handleWindow, win32con.SW_RESTORE)
            win32gui.ShowWindow(handleWindow, win32con.SW_SHOW)
            win32gui.SetForegroundWindow(handleWindow)
            print(f'I found the {appName}. It should be on your screen.')
            return True
    result = win32gui.EnumWindows(callback, None)
    if not result:
        print("No suitable matches found for", appName)

def sendMsg(msg):
    flag = False
    try:
        if 'online' in status and flag == False:
            textArea = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
            textArea.send_keys(msg)
            wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')))
            sendBtn = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
            flag = True
        elif 'online' not in status:
            print('User is not online')
            flag = False
    except:
        print('User is not online (ex)')
        flag = False

clickPerson('The person you want to send a message')
sleep(2)
while True:
    isOnline()
    sendMsg('This message send with WhatBot by ademcdev')
    sendMsg('Source Code: https://github.com/ademcdev')
    sleep(10)