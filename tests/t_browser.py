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

    def test_text_wrapping(self):
        text = f''' Beavers live in [freshwater ecosystems](/wiki/Freshwater_ecosystems "Freshwater ecosystems") such as rivers, streams, lakes and ponds. Water is the most important component of beaver habitat; they swim and dive in it, and it provides them refuge from land predators. It also restricts access to their homes and allows them to move building objects more easily. Beavers prefer slower moving streams, typically with a [gradient](/wiki/Stream_gradient "Stream gradient") (steepness) of one percent, though they have been recorded using streams with gradients as high as 15 percent. Beavers are found in wider streams more often than in narrower ones. They also prefer areas with no regular flooding and may abandon a location for years after a significant flood.[[47]](#cite_note-FOOTNOTEMüller-SchwarzeSun2003107,_109-47)
                    # Beavers typically select flat landscapes with diverse vegetation close to the water. North American beavers prefer trees being 60 m (200 ft) or less from the water, but will roam several hundred meters to find more. Beavers have also been recorded in mountainous areas. [Dispersing](/wiki/Biological_dispersal "Biological dispersal") beavers will use certain habitats temporarily before finding their ideal home. These include small streams, temporary swamps, ditches, and backyards. These sites lack important resources, so the animals do not stay there permanently. Beavers have increasingly settled at or near human-made environments, including agricultural areas, [suburbs](/wiki/Suburbs "Suburbs"), [golf courses](/wiki/Golf_courses "Golf courses"), and shopping malls.[[48]](#cite_note-FOOTNOTEMüller-SchwarzeSun2003106–110-48)'''
        lines = text.split('\n')
        max_width = 100
        wrapped_lines = self.emulator.get_wrapped(lines, max_width=max_width)
        for l in wrapped_lines:
            self.assertTrue(len(l) <= max_width)

        joined_t1 = text.replace('\n', '')
        joined_t2 = ''.join(wrapped_lines)

        self.assertEqual(joined_t1, joined_t2)

    @classmethod
    def tearDownClass(cls):
        cls.emulator.driver.close()
        cls.emulator.driver.quit()

        print(f'done')


if __name__ == "__main__":
    TestBrowserEmulator.execute_all()