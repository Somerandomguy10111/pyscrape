import os.path
import time
from typing import Optional

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from markdownify import markdownify
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# -----------------------------------------------

class BrowserEmulator:
    def __init__(self, headless : bool = True):
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument(f"--load-extension={os.path.dirname(__file__)}/cookie_blocker")
        if headless:
            chrome_options.add_argument(f'--headless')
        self.driver = uc.Chrome(options=chrome_options)

    def visit(self, url : str, load_delay : float = 2):
        self.driver.get(url)
        time.sleep(load_delay)

    def type(self, text_box_idx : int, content : str):
        visible_text_inputs = self.get_textinputs(visible_only=True)
        target_box = visible_text_inputs[text_box_idx]
        target_box.send_keys(content + Keys.RETURN)

    # ------------------------------------
    # get

    def get_markdown(self, max_width : Optional[int] = None) -> str:
        md = markdownify(self.get_html())
        lines = md.split('\n')
        lines = [line for line in lines if line.strip()]
        if max_width:
            lines = self.get_wrapped(lines, max_width)
        return '\n'.join(lines)

    def get_html(self, only_displayed : bool = True) -> str:
        html_code = self.driver.page_source
        if only_displayed:
            soup = BeautifulSoup(html_code, "html.parser")
            for element in soup.find_all(attrs={"aria-hidden": "true"}):
                element.decompose()
            return str(soup)

        return html_code

    def get_textinputs(self, visible_only : bool = True) -> list[WebElement]:
        text_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
        if visible_only:
            text_inputs = [input_box for input_box in text_inputs if input_box.is_displayed()]
        return text_inputs

    def __del__(self):
        self.driver.quit()


    @staticmethod
    def get_wrapped(lines : list[str], max_width : int) -> list[str]:

        compacted_lines = []
        for line in lines:
            if len(line) <= max_width:
                compacted_lines.append(line)
            else:
                no_lines = len(line) // max_width + 1 if len(line) % max_width > 0 else 0
                remain = line
                for _ in range(no_lines):
                    compacted_lines.append(remain[:max_width])
                    remain = remain[max_width:]

        return compacted_lines



if __name__ == "__main__":
    w1 = "https://docs.ros.org/en/foxy/index.html"
    w2 = 'https://platform.openai.com/docs/libraries#community-libraries'
    w3 = 'https://www.youtube.com/'
    w4 = 'https://stackoverflow.com/questions/16731115/how-to-debug-a-python-segmentation-fault'

    be = BrowserEmulator()
    be.visit(url=w1)
    print(be.get_markdown(max_width=200))