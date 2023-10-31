from selenium import webdriver
from .base import FunctionalTest
from selenium.webdriver.common.by import By


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
        self.add_list_item('Get help')

        # She notices a "Share this list" option
        share_box = self.browser.find_element(
            By.CSS_SELECTOR, 
            'input[name="share"]'
        )
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )