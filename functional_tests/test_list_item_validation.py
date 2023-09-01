from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from unittest import skip
from .base import FunctionalTest



class ItemValidationTest(FunctionalTest):
   
    def test_cannot_add_empty_item(self):

        # Edith goes the home page and accidentally tries to submit
        # an empty list item, she hits enter on athe empty testbox.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID,'id_new_item').send_keys(Keys.ENTER)

        # The home page refreshes and There is an error message
        #  saying that the tist item can not be blank.
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR,'.has-error').text,
            "You can't add an empty list item"))

        # She tries again with some text for the item, which now works
        self.browser.find_element(By.ID,'id_new_item').send_keys('Buy milk')
        self.browser.find_element(By.ID,'id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy milk')


        # Perversely, She now decides to submit another blank item.
        self.browser.find_element(By.ID,'id_new_item').send_keys(Keys.ENTER)

        # She recieves a similar warning on the list page.
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR,'.has-error').text,
            "You can't add an empty list item"
        ))

        # She can correct it by filling some text in.
        self.browser.find_element(By.ID,'id_new_item').send_keys('Make tea')
        self.browser.find_element(By.ID,'id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy milk')
        self.wait_for_row_in_list_table('2:Make tea')

        



