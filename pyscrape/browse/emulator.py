import undetected_chromedriver as uc
from markdownify import markdownify
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# -----------------------------------------------

class BrowserEmulator:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--load-extension=/home/daniel/.config/google-chrome/Default/Extensions/edibdbjcniadpccecjdfdjjppcpchdlm/1.1.4_0")
        self.driver = uc.Chrome(options=chrome_options)

    def visit(self, url : str):
        self.driver.get(url)

    def type(self, text_box_idx : int, content : str):
        text_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
        visible_text_inputs = [input_box for input_box in text_inputs if input_box.is_displayed()]
        target_box = visible_text_inputs[text_box_idx]
        target_box.send_keys(content + Keys.RETURN)

    # ------------------------------------
    # get current content

    def get_markdown(self) -> str:
        md = markdownify(self.get_html())
        lines = md.split('\n')
        cleaned = [line for line in lines if line.strip()]
        return '\n'.join(cleaned)

    def get_html(self, only_displayed : bool = True) -> str:
        def is_hidden(element):
            return element.get_attribute('aria-hidden') == 'true'

        if only_displayed:
            html_code = ''
            elements = self.driver.find_elements(By.XPATH, "//*")
            # top_hidden_elements = [element for element in elements if is_hidden(element)]
            for e in elements:
                html_code += e.get_attribute('outerHTML')
        else:
            html_code = self.driver.page_source
        return html_code

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
    be.visit(url=w4)
    print(be.get_markdown())