# STQA Mini Project - Black-box UI automation with Selenium WebDriver
# Tests the login page (login.html) with valid / invalid / empty / wrong-format inputs.
#
# Setup : pip install selenium      (Selenium 4.6+ downloads the Chrome driver automatically)
# Run   : python selenium_login_test.py
import os
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By

PAGE = "file:///" + os.path.abspath(os.path.join(os.path.dirname(__file__), "login.html")).replace("\\", "/")


class LoginPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()       # or webdriver.Firefox() / webdriver.Edge()
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def login(self, user, pwd):
        d = self.driver
        d.get(PAGE)
        d.find_element(By.ID, "username").send_keys(user)
        d.find_element(By.ID, "password").send_keys(pwd)
        d.find_element(By.ID, "loginBtn").click()
        time.sleep(0.5)                       # only so the examiner can see it
        return d.find_element(By.ID, "msg").text

    def test_TC_UI_01_page_title(self):
        self.driver.get(PAGE)
        self.assertEqual(self.driver.title, "Library Login")

    def test_TC_UI_02_valid_login(self):
        self.assertEqual(self.login("M1234", "lib@123"), "Welcome M1234")
        self.assertEqual(self.driver.title, "Library Dashboard")

    def test_TC_UI_03_wrong_password(self):
        self.assertEqual(self.login("M1234", "wrong"), "Invalid credentials")

    def test_TC_UI_04_empty_fields(self):
        self.assertEqual(self.login("", ""), "All fields are required")

    def test_TC_UI_05_invalid_id_format(self):
        self.assertEqual(self.login("abc", "lib@123"), "Invalid Member ID format")


if __name__ == "__main__":
    unittest.main(verbosity=2)
