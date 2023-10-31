from selenium import webdriver
from .base import FunctionalTest
from selenium.webdriver.common.by import By
from .list_page import ListPage
from .my_lists_page import MyListsPage


def quit_if_possible(browser):
    try: browser.quit()
    except: pass


class SharingTest(FunctionalTest):

    def test_can_share_a_list_with_another_user(self):
        # Aysha is a logged-in user
        self.create_pre_authenticated_session('aysha@example.com')
        aysha_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(aysha_browser))

        # Her friend Arwa is also hanging out on the lists site
        arwa_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(arwa_browser))
        self.browser = arwa_browser
        self.create_pre_authenticated_session('arwa@example.com')

        # Aysha goes to the home page and starts a list
        self.browser = aysha_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')
        

        # She notices a "Share this list" option
        share_box = list_page.get_share_box()
        
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        # She shares her list.
        # The page updates to say that it's shared with Arwa:
        list_page.share_list_with('arwa@example.com')

        # Arwa now goes to the lists page with his browser
        self.browser = arwa_browser
        MyListsPage(self).go_to_my_lists_page()

        # He sees Aysha's list in there!
        self.browser.find_element(By.LINK_TEXT, 'Get help').click()

        # On the list page, Arwa can see says that it's Aysha's list
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'aysha@example.com'
        ))

        #She adds an item to the list
        list_page.add_list_item('Hi Aysha!')

        # When Aysha refreshes the page, she sees Arwa's addition
        self.browser = aysha_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Aysha!', 2)