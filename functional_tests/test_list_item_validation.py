from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest



class ItemValidationTest(FunctionalTest):
   
    def test_cannot_add_empty_item(self):

        # Edith goes the home page and accidentally tries to submit
        # an empty list item, she hits enter on athe empty testbox.

        # The home page refreshes and There is an error message
        #  saying that the tist item can not be blank.

        # She tries again with some text for the item, which now works

        # Perversely, She now decides to submit another blank item.

        # She recieves a similar warning on the list page.

        # She can correct it by filling some text in.

        self.fail('write me!')



