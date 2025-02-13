import os.path

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from markdownify import markdownify
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


# -----------------------------------------------

class BrowserEmulator:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument(f"--load-extension={os.path.dirname(__file__)}/cookie_blocker")
        self.driver = uc.Chrome(options=chrome_options)

    def visit(self, url : str):
        self.driver.get(url)

    def type(self, text_box_idx : int, content : str):
        visible_text_inputs = self.get_textinputs(visible_only=True)
        target_box = visible_text_inputs[text_box_idx]
        target_box.send_keys(content + Keys.RETURN)

    # ------------------------------------
    # get

    def get_markdown(self) -> str:
        md = markdownify(self.get_html())
        lines = md.split('\n')
        cleaned = [line for line in lines if line.strip()]
        return '\n'.join(cleaned)

    def get_html(self, only_displayed : bool = True) -> str:
        html_code = self.driver.page_source
        if only_displayed:
            soup = BeautifulSoup(html_code, "html.parser")
            for element in soup.find_all(attrs={"aria-hidden": "true"}):
                element.decompose()
            return str(soup)

        return html_code

    def get_textinputs(self, visible_only : bool) -> list[WebElement]:
        text_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
        if visible_only:
            text_inputs = [input_box for input_box in text_inputs if input_box.is_displayed()]
        return text_inputs

    def __del__(self):
        self.driver.quit()


# Recognizing (visible) links
# links = driver.find_elements(By.TAG_NAME, 'a')
# visible_links = [link for link in links if link.is_displayed()]
# invisble_links = [link for link in links if not link.is_displayed()]
#
# print(f'- Visible links')
# for link in visible_links:
#     print(link.get_attribute('href'))
#
# print(f'- Invisible links')
# for link in invisble_links:
#     print(link.get_attribute('href'))

# Recognizing and interacting with (visible) text inputs



if __name__ == "__main__":
    w1 = "https://docs.ros.org/en/foxy/index.html"
    w2 = 'https://platform.openai.com/docs/libraries#community-libraries'
    w3 = 'https://www.youtube.com/'
    w4 = 'https://stackoverflow.com/questions/16731115/how-to-debug-a-python-segmentation-fault'

    be = BrowserEmulator()
    be.visit(url=w1)
    print(be.get_markdown())