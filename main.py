#!/usr/bin/env python
import logging
import threading

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from telegram.ext import Updater

from creditionals import *


def initTelegramBot():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    return Updater(token=TOKEN_TELEGRAM_BOT)


def session():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
    driver.get('https://twitter.com/login')
    return driver


def auth(driver):
    email = driver.find_element_by_name('session[username_or_email]')
    email.send_keys(USARNAME)
    password = driver.find_element_by_name('session[password]')
    password.send_keys(ACCESS_KEY, Keys.ENTER)


def target(driver):
    driver.get(TWITTER_TARGET)
    driver.implicitly_wait(4)


def lastTwit(driver):
    driver.find_elements_by_css_selector("[aria-label='Поделиться твитом']")[1].click()
    driver.find_element_by_xpath('//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/div[3]').click()
    return pyperclip.paste()


def writeHistory(history, twit):
    history.seek(0)
    history.truncate()
    history.write(twit)


def sendTwit(updater, driver, history):
    twit = lastTwit(driver)
    if twit.find('http') != -1 and twit != history.read():
        updater.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=twit)
        writeHistory(history, twit)


def schedule():
    return threading.Timer(15.0, sendTwit).start()


def main():
    driver = session()
    updater = initTelegramBot()

    auth(driver)
    target(driver)

    history = open('history.txt', 'r+')
    sendTwit(updater, driver, history)
    history.close()

    # schedule()
    return 0


if __name__ == "__main__":
    main()
