from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from unittest import skip
from .base import FunctionalTest



class ItemValidationTest(FunctionalTest):
   
    def test_cannot_add_empty_item(self):

        # Edith goes the home page and accidentally tries to submit
        # an empty list item, she hits enter on athe empty testbox.
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load
        # the list page
        self.wait_for(lambda: 
            self.browser.find_element(By.CSS_SELECTOR,'#id_text:invalid')
            )

        # She tries again with some text for the item, and error disappears
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: 
            self.browser.find_element(By.CSS_SELECTOR,'#id_text:valid')
            )
        
         # She submits it successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy milk')


        # Perversely, She now decides to submit another blank item.
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Again the browser will comply
        self.wait_for(lambda: 
            self.browser.find_element(By.CSS_SELECTOR,'#id_text:invalid')
            )

        # She can correct it by filling some text in.
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: 
            self.browser.find_element(By.CSS_SELECTOR,'#id_text:valid')
            )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy milk')
        self.wait_for_row_in_list_table('2:Make tea')

        



