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

    def  check_for_row_in_list_table(self,row_text):
        table = self.browser.find_element(By.ID,"id_list_table")
        rows = table.find_elements(By.TAG_NAME,"tr")
        self.assertIn(
            row_text ,
            [row.text for row in rows]
            )



    
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

        self.check_for_row_in_list_table("1:buy rice")



        #there is still a text box inviting it to enter another item
        #she enters buy tomatos to make fatah
        input_box = self.browser.find_element(By.ID,'id_new_item')
        input_box.send_keys("buy tomatos")
        input_box.send_keys(Keys.ENTER)
        time.sleep(3)

        #the page updates again and now shows the two items in the list
        self.check_for_row_in_list_table("1:buy rice")
        self.check_for_row_in_list_table("2:buy tomatos")
        
        #self.fail("Finish the test")
        #she goes back to sleep

if __name__ == "__main__":
    unittest.main()



        

