# Generate HTML in string from URL

```python
# One Single Page Websites also work
# Get html from page
from scraping.scraper import PageSources

page = PageSources('url...')

print(page.get_current_html())
```

---

```python
# save data in a directory call web_data
from scraping.scraper import PageSources

page = PageSources('https://andycode.ga/contact')
page.get_current_html()
page.save()
# page.save(directory='web_page') default
```

    When create a file it'll get name of hostPage and amount of file in your directory, like:
    -> web_data
        -hostPage_1.html
        -hostPage_2.html
        -hostPage_3.html
        ...

---

## It need a Google Chrome Driver

### To check the version you have of Google Chrome, you can do it from the browser information and in the "Help" section:

- Open a window in the browser.
- Go to the three points in the upper right.
- Choose the "Help" option from the drop-down menu.
- Tap on "Google Chrome Information"

---

### Go to https://chromedriver.chromium.org/downloads select your version, system and download

### It will be a file like this:

<img src="https://i.ibb.co/6Hfy3M6/Screenshot-2021-07-12-001416.png"  title="hover text">

### **Copy and paste in your root project**
