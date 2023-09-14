from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from unittest import skip
from .base import FunctionalTest



class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element(By.CSS_SELECTOR, '.has-error')
   
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

    def test_cannot_add_duplicate_items(self):

        # Edith goes to home page and starts a new list
        self.browser.get(self.live_server_url)  
        self.get_item_input_box().send_keys('Buy carrots')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy carrots')

        # she accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('Buy carrots')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # she sees a helpful error message
        self.wait_for(lambda:self.assertEqual(
            self.get_error_element().text,
            "you 've already got this in your list"
        ))     

    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error:
        self.browser.get(self.live_server_url)  
        self.get_item_input_box().send_keys('Buy carrots')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy carrots')
        self.get_item_input_box().send_keys('Buy carrots')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # she sees a helpful error message
        self.wait_for(lambda:self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        #she starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')

        # she is pleased to see that the error message disappears
        self.wait_for(lambda:self.assertFalse(
            self.get_error_element().is_displayed()
        ))

