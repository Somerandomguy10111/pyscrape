import time

from holytools.devtools import Unittest

from pyscrape.browse import BrowserEmulator


# -------------------------------------------------

class TestBrowserEmulator(Unittest):
    @classmethod
    def setUpClass(cls):
        cls.emulator = BrowserEmulator(headless=False)

    def test_bypass_bot_detection(self):
        test_url = 'https://platform.openai.com/docs/libraries#community-libraries'
        self.emulator.visit(url=test_url)

        html_code = self.emulator.get_html()

        self.assertTrue('Models' in html_code)
        self.assertTrue('Docs' in html_code)

    @classmethod
    def tearDownClass(cls):
        cls.emulator.driver.close()
        cls.emulator.driver.quit()


if __name__ == "__main__":
    TestBrowserEmulator.execute_all(trace_resourcewarning=True)