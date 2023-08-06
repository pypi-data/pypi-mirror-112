import os
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
        self.__url = url
        self.__chrome = webdriver.Chrome(chrome_options=self.options)
        self.__error = 40

    def get_current_html(self):
        """
        It will take a while.
        """
        try:
            print('Loading html...\n')
            self.__chrome.get(self.__url)
            if len(self.__chrome.page_source) < self.__error:
                raise Exception('Page not found')    
            return self.__chrome.page_source.encode("utf-8") # html in string
        except:
            raise Exception('schema http or https, TLD required, max length 2083')
    
    def getHostPageName(self):
        return self.__url[self.__url.find('//')+2:self.__url.find('.')]

    def closeBrowser(self):
        self.__chrome.close()
        return True

    def save(self, directory='web_data'):
        # root save directory
        path = os.getcwd()
        path_dir = f'{path}/{directory}'
        if not os.path.exists(path_dir):
            os.mkdir(path_dir)
        with open(f"{path_dir}/{self.getHostPageName()}_{len(os.listdir(path_dir))+1}.html", "w", encoding='utf-8') as code:
            code.write(f'{self.__chrome.page_source}')
            code.close()