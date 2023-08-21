from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time


MAX_WAIT = 5
class MyVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self,row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    
    def test_can_start_a_todo_list(self):
        #she goes to check the home page
        self.browser.get(self.live_server_url)

        #she notice the page title
        self.assertIn ('To-Do' ,self.browser.title) 
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn ('To-Do' ,header_text) 

        #she invited to enter a to-do Item straight away
        input_box = header_text = self.browser.find_element(By.ID,'id_new_item')
        self.assertEquals(input_box.get_attribute("placeholder"),"Enter a to-do item")
        
        #she typed buy rice in text box
        input_box.send_keys("buy rice")

        #when she hits enter the page update and now the item list
        #"1:buy rice"
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1:buy rice")

        #there is still a text box inviting it to enter another item
        #she enters buy tomatos to make fatah
        input_box = self.browser.find_element(By.ID,'id_new_item')
        input_box.send_keys("buy tomatos")
        input_box.send_keys(Keys.ENTER)
        

        #the page updates again and now shows the two items in the list
        self.wait_for_row_in_list_table("1:buy rice")
        self.wait_for_row_in_list_table("2:buy tomatos")
        
        #self.fail("Finish the test")
        #she goes back to sleep





    def test_multiple_users_can_start_lists_at_diff_urls(self):
        
        #Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element(By.ID,'id_new_item')
        input_box.send_keys("buy rice")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1:buy rice")

        #she notices that her list has a uniqe url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url,"/lists/.+")

        # Now a new user, Mizo, comes along to the site

        # We delete all the browser's cookies 
        # to simulate a brand new user session
        self.browser.delete_all_cookies()

        # Mizo visits the home page, There is no sign of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME,"body")
        self.assertNotIn("buy rice", page_text)
        self.assertNotIn("make fatah", page_text)

        # Mizo starts a new list by adding an item
        # He is less interesting than Edith
        input_box = self.browser.find_element(By.ID,'id_new_item')
        input_box.send_keys("buy milk")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1:buy milk")

        # Mizo gets his own uniqe url
        Mizo_list_url = self.browser.current_url
        self.assertRegex(Mizo_list_url,"/lists/.+")
        self.assertNotEqual(edith_list_url, Mizo_list_url)

        # Again There is no trace to Edith's list
        page_text = self.browser.find_element(By.TAG_NAME,"body")
        self.assertNotIn("buy rice", page_text)
        self.assertIn("buy milk", page_text)


        



