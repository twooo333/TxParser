#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException

from io import open
import time
import sys

def read_login_info(driver, info_file = None):
    try:
        if info_file:
            f = open(info_file, 'r')
        else:
            f = open('login_info', 'r')
        info = f.readlines()
    except FileNotFoundError:
        print('No login info file!')
        raise FileNotFoundError

    # find the element that's name attribute is q (the google search box)
    ID = driver.find_element_by_id("ctl00_ctl00_ContentPlaceHolder1_DefaultContent_id")
    usercode = driver.find_element_by_id("ctl00_ctl00_ContentPlaceHolder1_DefaultContent_usercode")
    password = driver.find_element_by_id("ctl00_ctl00_ContentPlaceHolder1_DefaultContent_PWD")
    
    ID.send_keys(info[0])
    usercode.send_keys(info[1])
    password.send_keys(info[2])    
    f.close()    

def auto_login():
    # Create a new instance of the Firefox driver
    if len(sys.argv) != 2:
        print 'Wrong argument number. One Argument please and 1 for PhantomJs, 2 for Firefox 43'
    else:
        if sys.argv[1] == '1':
            driver = webdriver.PhantomJS()
        elif sys.argv[1] == '2':
            driver = webdriver.Firefox()
        else:
            print "Wrong Argument input 1 for PhantomJs, 2 for Firefox 43"     

    # go to the google home page
    driver.get("https://mma.sinopac.com/MemberPortal/Member/NextWebLogin.aspx")

    # the page is ajaxy so the title is originally this:
    title = driver.title
    print(title)

    try:
        read_login_info(driver)
        login_button = driver.find_element_by_id("LoginBtn") 
        login_button.click()
        
        #wait for the login page is ready
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, '往來明細'))
        )
    except TimeoutException:
        print("Login Timeout!")
        driver.quit()
        driver = None
    except Exception:
        print("Login fail!")
        driver.quit()
        driver = None

    return driver
    
def output_result(driver):
    detail_link = driver.find_element_by_link_text('往來明細')
    detail_link.click()
    weekly_link = driver.find_element_by_link_text('最近一週')
    weekly_link.click()

	#wait for the result
    time.sleep(2)
    source_html = driver.page_source

    with open("./login.log",'w', encoding='utf8') as file:
        file.write(source_html)
    file.close()

	#logout to prevent next time login fail
    logout_link = driver.find_element_by_link_text('會員登出')
    logout_link.click()
    driver.quit() # Quit the driver and close every associated window.
    driver = None

if __name__ == '__main__':
    driver = auto_login()
    if driver:
        output_result(driver)
