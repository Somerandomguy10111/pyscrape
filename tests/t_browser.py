import time

from holytools.devtools import Unittest

from pyscrape.browse import BrowserEmulator


# -------------------------------------------------

class TestBrowserEmulator(Unittest):
    @classmethod
    def setUpClass(cls):
        cls.emulator = BrowserEmulator(headless=False)
        cls.emulator.driver.close()
        cls.emulator.driver.quit()

    def testsmth(self):
        pass

    # def test_bypass_bot_detection(self):
    #     test_url = 'https://platform.openai.com/docs/libraries#community-libraries'
    #     self.emulator.visit(url=test_url)
    #
    #     html_code = self.emulator.get_html()
    #
    #     self.assertTrue('Models' in html_code)
    #     self.assertTrue('Docs' in html_code)
    #
    #     self.emulator.driver.close()
    #     self.emulator.driver.quit()

    # @classmethod
    # def tearDownClass(cls):
    #
    #     time.sleep(2)


if __name__ == "__main__":
    TestBrowserEmulator.execute_all(trace_resourcewarning=True)