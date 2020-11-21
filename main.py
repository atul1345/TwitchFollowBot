import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import log
import credential_gen
import time

user_to_follow = open('user.txt', 'r').read()

tor = False

if tor:
    log.info('Getting Tor binary...')
    binary = '/Applications/Tor Browser.app/Contents/MacOS/firefox'
    if os.path.exists(binary) is False:
        raise ValueError("The binary path to Tor firefox does not exist.")
    firefox_binary = FirefoxBinary(binary)
    firefox_binary.add_command_line_options()

    log.info('Starting Tor...')
    browser = webdriver.Firefox(firefox_binary=firefox_binary)
    log.good('Tor started!')
else:
    log.info('Starting Chrome...')
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=chrome_options)
    log.good("Chrome started!")

# Start

# Gen credentials
credentials = credential_gen.gen_credentials()
username = credentials[0]
password = credentials[1]
date_of_birth = credentials[2]
email = credentials[3]

# Start browser
log.info('Getting twitch.tv...')
browser.get("https://twitch.tv")

sign_up_button = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/nav/div/div[3]/div[3]/div/div[1]/div[2]/button')
sign_up_button.click()
log.good("Clicked signup button...")

log.info("Waiting to load signup form...")
time.sleep(3)

# Sign up

# Username
username_field = browser.find_element_by_xpath('//*[@id="signup-username"]')
username_field.send_keys(username)
log.good(f'Filled in username: {username}')

# Password
password_field = browser.find_element_by_xpath('//*[@id="password-input"]')
password_field.send_keys(password)
log.good(f'Filled in password: {password}')

# Confirm password
confirm_password_field = browser.find_element_by_xpath('//*[@id="password-input-confirmation"]')
confirm_password_field.send_keys(password)
log.good(f'Filled in confirmed password: {password}')

# Date of birth
month = browser.find_element_by_xpath(f'/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div[3]/form/div/div[3]/div/div[2]/div[1]/select/option[{date_of_birth[0]+1}]').click()
day = browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div[3]/form/div/div[3]/div/div[2]/div[2]/div/input').send_keys(date_of_birth[1])
year = browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div[3]/form/div/div[3]/div/div[2]/div[3]/div/input').send_keys(date_of_birth[2])

# Email
email_field = browser.find_element_by_xpath('//*[@id="email-input"]')
email_field.send_keys(email)
log.good(f'Filled in email: {email}')

log.info('Waiting for submission verification...')
time.sleep(2)

# Submit form
submit_button = browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div[3]/form/div/div[5]/button')
submit_button.click()
log.good('Submitted sign up form.')

log.info("Waiting 3 seconds...")
time.sleep(3)

# Remind to verify later
remind_later = browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div/div/div[3]/div[2]/div/button')
remind_later.click()
log.good('Skipped email verification...')

log.info("Waiting 3 seconds...")
time.sleep(3)
browser.get(f'https://twitch.tv/{user_to_follow}')

time.sleep(1)

# Follow
follow_button = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div/button')
follow_button.click()
log.good(f"Followed {user_to_follow}!")