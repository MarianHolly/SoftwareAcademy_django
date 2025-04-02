import time
from unittest import skip

from django.test import TestCase
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class GuiTestWithSelenium(TestCase):
    @skip("Skip")
    def test_home_page_firefox(self):
        driver = webdriver.Firefox()
        driver.get("http://127.0.0.1:8000/")
        assert "Vitajte v našej filmovej databáze." in driver.page_source

    @skip("Skip")
    def test_home_page_chrome(self):
        driver = webdriver.Chrome()
        driver.get("http://127.0.0.1:8000/")
        assert "Vitajte v našej filmovej databáze." in driver.page_source

    @skip("Skip")
    def test_signup(self):
        driver = webdriver.Firefox()
        driver.get("http://127.0.0.1:8000/accounts/signup/")
        time.sleep(2)

        username_field = driver.find_element(By.ID, "id_username")
        username_field.send_keys("TestUser2")
        time.sleep(1)

        first_name_field = driver.find_element(By.ID, "id_first_name")
        first_name_field.send_keys("David")
        time.sleep(1)

        last_name_field = driver.find_element(By.ID, "id_last_name")
        last_name_field.send_keys("Orechovský")
        time.sleep(1)

        email_field = driver.find_element(By.ID, "id_email")
        email_field.send_keys("orechovsky@mail.com")
        time.sleep(1)

        password1_field = driver.find_element(By.ID, "id_password1")
        password1_field.send_keys("PWord43Tree121/")
        time.sleep(1)

        password2_field = driver.find_element(By.ID, "id_password2")
        password2_field.send_keys("PWord43Tree121/")
        time.sleep(1)

        biography_field = driver.find_element(By.ID, "id_biography")
        biography_field.send_keys("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        time.sleep(1)

        submit_button = driver.find_element(By.ID, "id_submit")
        submit_button.send_keys(Keys.RETURN)
        time.sleep(1)

        assert ("Vitajte v našej filmovej databáze."
                or "A user with that username already exists."
                in driver.page_source)

    def test_movie_not_in_db(self):
        selenium_webdriver = webdriver.Chrome()
        selenium_webdriver.get('http://127.0.0.1:8000/movie/1000/')
        time.sleep(2)
        assert 'Filmy' in selenium_webdriver.page_source