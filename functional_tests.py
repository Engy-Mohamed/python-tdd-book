from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest


class MyVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()
    
    def test_can_start_a_todo_list(self):
        #she goes to check the home page
        self.browser.get('http://localhost:8000')

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
        time.sleep(3)

        table = self.browser.find_element(By.ID,"id_list_table")
        rows = table.find_elements(By.TAG_NAME,"tr")
        self.assertTrue(any(row.text == "1:buy rice" for row in rows))


        #there is still a text box inviting it to enter another item
        #she enters buy tomatos to make fatah

        #the page updates again and now shows the two items in the list
        self.fail("Finish the test")
        #she goes back to sleep

if __name__ == "__main__":
    unittest.main()



        

