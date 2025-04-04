# -*- coding: utf-8 -*-

from os.path import isfile, realpath, dirname
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import run
from datetime import date
import time
import requests

# Clear terminal function
def clear():
    run('cls' if os.name == 'nt' else 'clear', shell=True)

# Directory of the script
script_dir = dirname(realpath(__file__))

# Status messages
messages = [
    "User Data: ",
    "Automated Browser: ",
    "Renewal: ",
    "Consultation: ",
    "Due Date: ",
    "Scheduled Renewal: "
]

def status(step):
    clear()
    for i in range(step):
        print(messages[i] + "OK")

def bot(username, password, renew=True, consult=True):
    # Browser automation setup
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    browser = webdriver.Chrome(service=service, options=options)
    browser.get("http://virtua.uel.br:8080/auth/login?")
    status(1)
    time.sleep(4)

    browser.find_element(By.NAME, "username").send_keys(username)
    browser.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)
    time.sleep(3)

    if renew:
        browser.find_element(By.NAME, "button.selectAll").click()
        browser.find_element(By.ID, "button.renew").click()
        status(2)
        time.sleep(3)

    due_dates = []
    if consult:
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        books = soup.select("table tbody tr td:nth-child(4) div")
        due_dates = [book.text.strip() for book in books]

    browser.quit()
    status(3)
    return due_dates

def find_due_date(dates):
    dates.sort(key=lambda d: [int(x) for x in d.split('/')][::-1])
    next_due_date = dates[0] if dates else None
    status(4)
    print(f"Next execution date: {next_due_date}")
    return next_due_date

def schedule_task(due_date):
    today = date.today().strftime("%d/%m/%Y")
    if today == due_date:
        due_date = find_due_date(user_file())
        if not isfile('renew.txt'):
            run(['schtasks', '/create', '/tn', 'Renew Books', '/tr', 'python autoBC.py', '/sc', 'ONCE', '/sd', due_date, '/st', '08:00', '/f'])
            status(5)
            with open('renew.txt', 'w') as file:
                file.write(due_date)
        else:
            run(['schtasks', '/change', '/tn', 'Renew Books', '/sd', due_date, '/st', '08:00', '/f'])
        print(f"Next execution date: {due_date}")
    else:
        print(f"Next execution date: {due_date}")

def user_file():
    if isfile('user.txt'):
        with open('user.txt', 'r') as file:
            user = file.readline().strip()
            password = file.readline().strip()
        status(0)
        return bot(user, password, renew=True, consult=True)
    return []

if not isfile('user.txt'):
    print("No registered user found. Please enter details.")
    user = input("Enter barcode: ")
    password = input("Enter password: ")
    with open('user.txt', 'w') as file:
        file.write(user + '\n' + password + '\n')
    due_dates = bot(user, password, renew=False, consult=True)
    due_date = find_due_date(due_dates)
elif isfile("renew.txt"):
    with open('renew.txt', 'r') as file:
        due_date = file.readline().strip()
    schedule_task(due_date)
else:
    schedule_task(date.today().strftime("%d/%m/%Y"))

input("Press any key to exit...")
