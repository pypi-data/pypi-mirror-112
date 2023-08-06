from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pydantic import HttpUrl

class PageSources():
    #Config
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')

    def __init__(self, url: HttpUrl):
        self.url = url
        self.chrome = webdriver.Chrome(chrome_options=self.options)
        self.error = 40

    def get_current_html(self):
        """
        It will take a while.
        """
        try:
            self.chrome.get(self.url)
            if len(self.chrome.page_source) < 40:
                raise Exception('Page not found')    
            return self.chrome.page_source # html in string
        except:
            raise Exception('schema http or https, TLD required, max length 2083')
        finally:
            self.chrome.close()