import base64
import json
import logging
import os
import requests
import subprocess
import time
import uuid

import io
import PIL
from PIL import Image

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains

from appium import webdriver

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

URL = 'https://fluffy-dragon.test.ai'

class TestAiDriver():
    def __init__(self, driver, api_key):
        self.driver = driver
        self.api_key = api_key
        self.run_id = str(uuid.uuid1())


        window_size = self.driver.get_window_size()
        screenshotBase64 = self.driver.get_screenshot_as_base64()
        im = Image.open(io.BytesIO(base64.b64decode(screenshotBase64)))
        width, height = im.size
        self.multiplier = 1.0 * width / window_size['width']

        self_attrs = dir(self)
        for a_name in dir(driver):
            if a_name in self_attrs:
                continue
            try:
                def _call_driver(_name=a_name, **kwargs):
                    v = getattr(self.driver, _name)
                    return v(**kwargs)

                v = getattr(self.driver, a_name)
                if hasattr(v, '__call__'):
                    setattr(self, a_name, _call_driver)
                else:
                    setattr(self, a_name, v)
            except Exception:
                continue


    def implicitly_wait(self, wait_time):
        self.driver.implicitly_wait(wait_time)

    def find_element(self, by='id', value=None, element_name=None):
        """
        Find an element given a By strategy and locator.
        :Usage:
            ::
                element = driver.find_element(By.ID, 'foo')
        :rtype: WebElement
        """
        key = None
        if element_name is not None:
            el, key = self._classify(element_name)
            if el is not None:
                return el

        # Run the standard selector
        el = self.driver.find_element(by=by, value=value)
        if element_name:
            self._update_elem(el, key, element_name)
        return el

    def find_element_by_accessibility_id(self, accessibility_id, element_name=None):
        """
        Finds an element by an accessibility id.

        :Args:
         - accessibility_id: The name of the element to find.
         - element_name: The label name of the element to be classified.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            ::
                element = driver.find_element_by_accessibility_id('foo')
        """
        key = None
        if element_name is not None:
            el, key = self._classify(element_name)
            if el is not None:
                return el

        # Run the standard selector
        el = self.driver.find_element_by_accessibility_id(accessibility_id)
        if element_name:
            self._update_elem(el, key, element_name)
        return el

    def find_element_by_class_name(self, name, element_name=None):
        """
        Finds an element by class name.

        :Args:
         - name: The class name of the element to find.
         - element_name: The label name of the element to be classified.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            ::
                element = driver.find_element_by_class_name('foo')
        """
        key = None
        if element_name is not None:
            el, key = self._classify(element_name)
            if el is not None:
                return el

        # Run the standard selector
        el = self.driver.find_element_by_class_name(name)
        if element_name:
            self._update_elem(el, key, element_name)
        return el

    def find_element_by_css_selector(self, css_selector, element_name=None):
        """
        Finds an element by css selector.

        :Args:
         - css_selector - CSS selector string, ex: 'a.nav#home'
         - element_name: The label name of the element to be classified.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            ::

                element = driver.find_element_by_css_selector('#foo')
        """
        key = None
        if element_name is not None:
            el, key = self._classify(element_name)
            if el is not None:
                return el

        # Run the standard selector
        el = self.driver.find_element_by_css_selector(css_selector)
        if element_name:
            self._update_elem(el, key, element_name)
        return el

    def find_element_by_id(self, id_, element_name=None):
        """
        Finds an element by id.

        :Args:
         - id\\_ - The id of the element to be found.
         - element_name: The label name of the element to be classified.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            ::

                element = driver.find_element_by_id('foo')
        """
        key = None
        if element_name is not None:
            el, key = self._classify(element_name)
            if el is not None:
                return el

        # Run the standard selector
        el = self.driver.find_element_by_id(id_)
        if element_name:
            self._update_elem(el, key, element_name)
        return el


    def find_element_by_link_text(self, link_text, element_name=None):
        """
        Finds an element by link text.

        :Args:
         - link_text: The text of the element to be found.
         - element_name: The label name of the element to be classified.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            ::

                element = driver.find_element_by_link_text('Sign In')
        """
        key = None
        if element_name is not None:
            el, key = self._classify(element_name)
            if el is not None:
                return el

        # Run the standard selector
        el = self.driver.find_element_by_link_text(link_text)
        if element_name:
            self._update_elem(el, key, element_name)
        return el


    def find_element_by_name(self, name, element_name=None):
        """
        Finds an element by name.

        :Args:
         - name: The name of the element to find.
         - element_name: The label name of the element to be classified.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            ::

                element = driver.find_element_by_name('foo')
        """
        key = None
        if element_name is not None:
            el, key = self._classify(element_name)
            if el is not None:
                return el

        # Run the standard selector
        el = self.driver.find_element_by_name(name)
        if element_name:
            self._update_elem(el, key, element_name)
        return el


    def find_element_by_partial_link_text(self, link_text, element_name=None):
        """
        Finds an element by a partial match of its link text.

        :Args:
         - link_text: The text of the element to partially match on.
         - element_name: The label name of the element to be classified.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            ::

                element = driver.find_element_by_partial_link_text('Sign')
        """
        key = None
        if element_name is not None:
            el, key = self._classify(element_name)
            if el is not None:
                return el

        # Run the standard selector
        el = self.driver.find_element_by_partial_link_text(link_text)
        if element_name:
            self._update_elem(el, key, element_name)
        return el


    def find_element_by_tag_name(self, name, element_name=None):
        """
        Finds an element by tag name.

        :Args:
         - name - name of html tag (eg: h1, a, span)
         - element_name: The label name of the element to be classified.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            ::

                element = driver.find_element_by_tag_name('h1')
        """
        key = None
        if element_name is not None:
            el, key = self._classify(element_name)
            if el is not None:
                return el

        # Run the standard selector
        el = self.driver.find_element_by_tag_name(name)
        if element_name:
            self._update_elem(el, key, element_name)
        return el


    def find_element_by_xpath(self, xpath, element_name=None):
        """
        Finds an element by xpath.

        :Args:
         - xpath - The xpath locator of the element to find.
         - element_name: The label name of the element to be classified.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            ::

                element = driver.find_element_by_xpath('//div/td[1]')
        """
        key = None
        if element_name is not None:
            el, key = self._classify(xpath)
            if el is not None:
                return el

        # Run the standard selector
        el = self.driver.find_element_by_xpath(name)
        if element_name:
            self._update_elem(el, key, element_name)
        return el


    def find_by_element_name(self, element_name):
        """
        Finds an element by element_name.

        :Args:=
         - element_name: The label name of the element to be classified.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            ::

                element = driver.find_element_by_xpath('//div/td[1]')
        """
        el, key = self._classify(element_name)
        if el is None:
            raise Exception('No element classified')
        # self._update_elem(el, key, element_name)
        return el

    def _update_elem(self, elem, key, element_name):
        data = {
            'key': key,
            'api_key': self.api_key,
            'run_id': self.run_id,
            'label': element_name,
            'x': elem.rect['x'] ,
            'y': elem.rect['y'],
            'width': elem.rect['width'],
            'height': elem.rect['height'],
            'multiplier': self.multiplier
        }
        try:
            action_url = URL + '/add_action'
            # Verify is False as the lets encrypt certificate raises issue on mac.
            _ = requests.post(action_url, data=data, verify=False)
        except Exception:
            pass

    def _classify(self, element_name):
        element = None
        run_key = None
        # Call service
        ## Get screenshot & page source
        screenshotBase64 = self.driver.get_screenshot_as_base64()

        # ZZZ
        with open('/tmp/scnshot.png', 'wb') as outFile:
            outFile.write(base64.b64decode(screenshotBase64))
        try:
            source = self.driver.page_source
        except Exception:
            source = ''

        # Check results
        try:
            data = {'screenshot': screenshotBase64, 'source': source,
                    'api_key':self.api_key, 'label': element_name, 'run_id': self.run_id}
            classify_url = URL + '/classify'
            r = requests.post(classify_url, data=data, verify=False)
            #print('r.text: %s', r.text)
            response = json.loads(r.text)
            run_key = response['key']
            if response.get('success', False):
                print('successful classification of element_name: %s' % element_name)
                pred_elem = response['elem']

                root_elem = self.driver.find_element_by_xpath("//*")
                element = testai_elem(root_elem.parent, root_elem._id, pred_elem, self.driver, self.multiplier)
                # Found elem, use image matcher
                # self.driver.update_settings({"getMatchedImageResult": True})
                # element = self.driver.find_element_by_image('/Users/chris/test_ai/api/next.png')
            else:
                logging.error('Classification failed for element_name: %s - Please visit %s to classify' % (element_name, URL+'/label/'+element_name))
        except Exception:
            logging.exception('exception during classification')
        return element, run_key


class testai_elem(webdriver.webelement.WebElement):
    def __init__(self, parent, _id, elem, driver, multiplier=1.0):
        super(testai_elem, self).__init__(parent, _id)
        self.driver = driver
        self._text = elem.get('text', '')
        self._size = {'width': elem.get('width', 0)/multiplier, 'height': elem.get('height', 0)/multiplier}
        self._location = {'x': elem.get('x', 0)/multiplier, 'y': elem.get('y', 0)/multiplier}
        self._property = elem.get('class', '')
        self._rect = self._size | self._location
        self._tag_name = elem.get('class', '')
        self._cx = elem.get('x', 0)/multiplier  + elem.get('width', 0) / multiplier / 2
        self._cy = elem.get('y', 0)/multiplier + elem.get('height', 0) /multiplier / 2


    @property
    def text(self):
        return self._text
    @property
    def size(self):
        return self._size
    @property
    def location(self):
        return self._location
    @property
    def rect(self):
        return self._rect
    @property
    def tag_name(self):
        return self._tag_name

    def click(self):
        self.driver.tap([(self._cx, self._cy)])

    def send_keys(self, value, click_first=True):
        if click_first:
            self.click()
        actions = ActionChains(self.driver)
        actions.send_keys(value)
        actions.perform()

    def submit(self):
        self.send_keys('\n', click_first=False)

    def clear(self):
        pass

    def is_selected(self):
        return True
    def is_enabled(self):
        return True
    def is_displayed(self):
        return True
