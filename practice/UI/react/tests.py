import os
import pathlib
import unittest
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

# Finds the Uniform Resourse Identifier of a file


def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()


# Sets up web driver using Google chrome
driver = webdriver.Chrome(executable_path="C:\Users\Aryan Enterprises\AppData\Local\Programs\Python\Python310\Lib\site-packages\chromedriver_py")
# Standard outline of testing class


class WebpageTests(unittest.TestCase):

    def test_title(self):
        """Make sure title is correct"""
        driver.get(file_uri("count.html"))
        self.assertEqual(driver.title, "Counter")

    def test_increase(self):
        """Make sure header updated to 1 after 1 click of increase button"""
        driver.get(file_uri("count.html"))
        increase = driver.find_element("count")
        increase.click()
        self.assertEqual(driver.find_element("h1").text, "1")

    def test_multiple_increase(self):
        """Make sure header updated to 3 after 3 clicks of increase button"""
        driver.get(file_uri("count.html"))
        increase = driver.find_element("count")
        for i in range(3):
            increase.click()
        self.assertEqual(driver.find_element("h1").text, "3")


if __name__ == "__main__":
    unittest.main()
