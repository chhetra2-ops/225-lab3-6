
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest


class TestH5Tag(unittest.TestCase):
    def setUp(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")

        self.driver = webdriver.Firefox(options=firefox_options)

    def test_h5_tag_content(self):
        driver = self.driver

        # DEV Ingress address reported by Jenkins
        driver.get("http://10.48.229.167/")

        h5_element = driver.find_element(By.TAG_NAME, "h5")
        h5_text = h5_element.text

        self.assertEqual(
            "Lab 3-6 Works!",
            h5_text,
            "The <h5> tag does not contain the text 'Lab 3-6 Works!'"
        )

    def tearDown(self):
        if hasattr(self, "driver"):
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()

