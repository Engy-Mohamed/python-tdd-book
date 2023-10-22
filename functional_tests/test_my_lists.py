from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from selenium.webdriver.common.by import By
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)
        
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):

        # Aysha is a logged-in user
        self.create_pre_authenticated_session('aysha@example.com')

        # She goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item('Set the stuff')
        self.add_list_item('Tide the things')
        first_list_url = self.browser.current_url

        # She notices a "My lists" link, for the first time.
        self.browser.find_element(By.LINK_TEXT, 'My lists').click()

        # She sees that her list is in there, named according to its
        # first list item
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Set the stuff')
        )
        self.browser.find_element(By.LINK_TEXT, 'Tide the things').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        self.add_list_item('Add a topic')
        second_list_url = self.browser.current_url

        # Under "my lists", her new list appears
        self.browser.find_element(By.LINK_TEXT, 'My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Add a topic')
        )
        self.browser.find_element(By.LINK_TEXT, 'Add a topic').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out.  The "My lists" option disappears
        self.browser.find_element(By.LINK_TEXT, 'Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements(By.LINK_TEXT, 'My lists'),
            []
        ))

