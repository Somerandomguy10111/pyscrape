import time

from holytools.devtools import Unittest

from pyscrape.browse import BrowserEmulator


# TODO: There is a known issue with undetected_chromedriver leaving spawned process alive after driver.quit()
# TODO: (https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/1270)
# TODO: As long as this issue is not addressed, expect a resource warning

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

    def test_cookie_blocker(self):
        test_url = 'https://www.youtube.com/'
        self.emulator.visit(url=test_url)
        site_content = self.emulator.get_html()
        self.assertFalse(f'Before you continue to YouTube' in site_content)

    @classmethod
    def tearDownClass(cls):
        cls.emulator.driver.close()
        cls.emulator.driver.quit()

        print(f'done')


if __name__ == "__main__":
    TestBrowserEmulator.execute_all()