import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Handywrapper:

    def __init__(self,driver):
        self.driver = driver


    def find_element(self,By_type, locator=""):
        element = ""
        try:
            element = self.driver.find_element(By_type, locator)
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            print(element)
            return element
        except:
            return element


    def get_attribute(self,By_type, locator="", att="value"):
        value = ""
        try:
            element = self.find_element(By_type, locator)
            value = element.get_attribute(att)
            return value
        except:
            return value


    def find_elements(self,By_type, locator=""):
        element_list = []
        try:
            element_list = self.driver.find_elements(By_type, locator)
            return element_list
        except:
            return element_list


    def get_list_of_attributes(self,By_type, locator="", att="value"):
        value_list = []
        try:
            element_list = self.find_elements(By_type, locator)
            for element in element_list:
                value = element.get_attribute(att)
                value_list.append(value)
            print(value_list)
            return value_list
        except:
            return value_list


    def get_element_tag(self, element=None, tag=""):
        try:
            element = element.find_element(By.TAG_NAME, tag)
            return element
        except:
            return ""


    def find_element_text(self,By_type="", locator="",element = None):
        try:
            if element !=None:
                element_text = element.text
            else:
                time.sleep(0.5)
                element = self.find_element(By_type, locator)
                element_text = element.text
            print(element_text)
            return element_text
        except:
            return ""


    def find_elements_list_of_text(self,By_type, locator=""):
        elements_list_of_text = []
        try:
            elements = self.find_elements(By_type, locator)
            for element in elements:
                elements_list_of_text.append(element.text)
            print(elements_list_of_text)
            return elements_list_of_text
        except:
            return []


    def Click_element(self,By_type="", locator="", element=None ):
        try:
            time.sleep(0.5)
            if element is not None:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                time.sleep(0.5)
                element.click()
            else:
                self.wait_explicitly(By_type, locator)
                element = self.find_element(By_type, locator)
                self.wait_explicitly(By_type, locator)
                # self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                time.sleep(0.5)
                element.click()
        except:
            print("cannot click the element")


    def is_element_present(self,By_type, locator=""):
        try:
            element = self.driver.find_element(By_type, locator)
            if element is not None:
                return True
            else:
                return False
        except:
            return False

    def wait_explicitly(self, By_type, locator="", timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By_type, locator)))
        except:
            pass

    def get_value_by_key(self, key, dict):
        try:
            value = dict[key]
            return value
        except:
            return ""
