import os
import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


class TwitterScrapper:
    def __init__(self, username, password, driver_name, driver_loc):
        self.username = username
        self.password = password
        self.driver_name = driver_name
        self.driver_location = driver_loc
        self.base_url = "https://twitter.com/"

        self.__setup_driver()

    def __setup_driver(self):
        if "chrome":
            self.driver = webdriver.Chrome(self.driver_location)
        else:
            print("Other driver not supported")

    def __is_logged(self):
        # get explore button because when u r not logged in
        # this button is not showed
        try:
            self.driver.find_element(By.XPATH, "//a[@data-testid='AppTabBar_Explore_Link']")
        except:
            self.__login_process()

    def __login_process(self):
        # open login form
        login_url = os.path.join(self.base_url, "i/flow/login")
        self.driver.get(login_url)

        # get username input
        username = self.driver.find_element(By.XPATH, "//input[@autocomplete='username']")
        username.send_keys(self.username)
        self.driver.find_element(By.XPATH, "//span[text()='Next']").click()

        # get password input
        password = self.driver.find_element(By.XPATH, "//input[@name='password']")
        password.send_keys(self.password)
        self.driver.find_element(By.XPATH, "//div[@data-testid='LoginForm_Login_Button']").click()

    def get_post(self, total_post, keyword, **kwargs):
        # check if user is logged in
        self.__is_logged()

        # open explore form
        self.driver.get(os.path.join(self.base_url, "explore"))

        # search by keyword
        search_box = self.driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
        search_box.send_keys(keyword)
        search_box.submit()

        # used for store post are crawled
        post_list = list()
        post_counter = 0

        while True:
            # get page source
            page = self.driver.page_source
            page_soup = BeautifulSoup(page, "lxml")
        
            # get account detail
            tweets = page_soup.find_all("article")
            for tweet in tweets:
                pass