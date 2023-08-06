# -*- coding: utf-8 -*-
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

options = webdriver.ChromeOptions()
options.headless = True


class Screenshot:
    def __init__(self, driver, url, port, jsdocument, tagname, screenshotname, showimage):
        """
        :param driver:
        :param url:
        :param port:
        :param jsdocument:
        :param tagname:
        :param screenshotname:
        :param showimage:
        """
        self.port = port
        self.tagname = tagname
        self.driver = driver
        self.screenshotname = screenshotname

        self.jsdocument = jsdocument
        if self.jsdocument == 'body':
            self.jsdocument = 'return document.body.parentNode.scroll'

        self.url = url
        self.showimage = showimage
        self.__optionsChrome = webdriver.ChromeOptions()
        self.__optionsFirefox = webdriver.FirefoxOptions()
        self.__optionsFirefoxProfile = webdriver.FirefoxProfile()

    def take_screenshot(self):

        if self.driver == 'chrome':
            self.__optionsChrome.headless = True
            self.driver = webdriver.Chrome(options=self.__optionsChrome)
        elif self.driver == 'firefox':
            self.driver = webdriver.Firefox()
        elif self.driver == 'edge':
            self.driver = webdriver.Edge()
        elif self.driver == 'opera':
            self.driver = webdriver.Opera(options=options)
        elif self.driver == 'safari':
            self.driver = webdriver.Safari()

        try:
            self.driver.get(self.url)
            def S(X): return self.driver.execute_script(self.jsdocument + X)
            self.driver.set_window_size(S('Width'), S('Height'))
            self.driver.find_element_by_tag_name(
                self.tagname,
            ).screenshot(self.screenshotname)
            if self.showimage:
                screenshot = Image.open(self.screenshotname)
                screenshot.show()
            else:
                pass
        except WebDriverException:
            print('ERR_NAME_NOT_RESOLVED')


"""test = Screenshot(driver='chrome',
                  url='https://stackoverflow.com/questions/21053738/add-header-to-fpdf',
                  port=443,
                  jsdocument='body',
                  tagname='body',
                  screenshotname="test.png",
                  showimage=True).take_screenshot()"""
