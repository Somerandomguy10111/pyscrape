from __future__ import annotations

from holytools.devtools import Unittest

from pyscrape.scrape import Scraper


class VisitorTester(Unittest):
    @classmethod
    def setUpClass(cls):
        cls.visitor = Scraper(headless=True)
        cls.beavers_url = 'https://en.wikipedia.org/wiki/Beaver'
        cls.invalid_url = 'https://asldkfjskdjdkkkkkk'
        cls.browser_required_url = 'https://leetcode.com/problemset/'
        cls.models_docs = 'https://platform.openai.com/docs/models'

    def test_driver(self):
        self.beaver_test()

    def test_link(self):
        link_text = self.visitor.scrape_text(url=self.beavers_url, with_links=True)
        self.assertIn('http', link_text)

    def test_exists(self):
        beavers_exists = self.visitor.site_exists(url=self.beavers_url)
        invalid_doesnt_exist = self.visitor.site_exists(url=self.invalid_url)
        model_docs_exist = self.visitor.site_exists(url=self.models_docs)
        self.assertTrue(beavers_exists)
        self.assertFalse(invalid_doesnt_exist)
        self.assertTrue(model_docs_exist)

    # -------------------------------------------

    def beaver_test(self):
        text = self.visitor.scrape_text(url=self.beavers_url)
        self.assertTrue(self.contains_beavers(text=text))
        self.log(f'Beaver text: {text[:500]}')

    @staticmethod
    def contains_beavers(text: str) -> bool:
        return 'beavers' in text.lower()


if __name__ == "__main__":
    VisitorTester.execute_all()