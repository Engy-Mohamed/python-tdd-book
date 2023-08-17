from selenium import webdriver
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

        #she invited to enter a to-do Item straight away
        self.fail("Finish the test")
        #she typed buy rice in text box

        #when she hits enter the page update and now the item list
        #"1:buy rice"

        #there is still a text box inviting it to enter another item
        #she enters buy tomatos to make fatah

        #the page updates again and now shows the two items in the list

        #she goes back to sleep

if __name__ == "__main__":
    unittest.main()



        

