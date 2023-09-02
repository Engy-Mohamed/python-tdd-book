
from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


    


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        

        # Edith goes to home page
        self.browser.get(self.live_server_url)

        # her browser window is set to a specific size
        self.browser.set_window_size(700, 768)

        # she notices the input box is nicely centered
        input_box = self.get_item_input_box()

        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            350,
            delta=10,
        )
        
        # She starts a new list ans sees the input is nicely centered
        input_box.send_keys("testing")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1:testing")
        
        input_box = self.get_item_input_box()

        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            350,
            delta=10,
        )

