from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response,"home.html")


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):

        mylist = List()
        mylist.save()
        
        first_item = Item()
        first_item.text = "the first list item"
        first_item.list = mylist
        first_item.save()

        second_item = Item()
        second_item.text = "the second list item"
        second_item.list = mylist
        second_item.save()

        savedList = List.objects.get()
        self.assertEqual(mylist,savedList)

        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(),2)

        first_saved_item = savedItems[0]
        second_saved_item = savedItems[1]

        self.assertEqual(first_saved_item.text,"the first list item")
        self.assertEqual(first_saved_item.list,mylist)
        self.assertEqual(second_saved_item.text,"the second list item")
        self.assertEqual(second_saved_item.list,mylist)

class ListViewTest(TestCase):
    def test_uses_test_template(self):
        mylist = List.objects.create()
        response = self.client.get(f'/lists/{mylist.id}/')
        self.assertTemplateUsed(response, "list.html")

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item", list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response,"itemey 1")
        self.assertContains(response,"itemey 2")
        self.assertNotContains(response,"other list item")
    
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context['list'],correct_list)
        
class NewListTest(TestCase):
    def test_can_save_a_post_request(self):
        self.client.post("/lists/new",data={"item_text":"A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")
        
        
    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new",data={"item_text":"A new list item"})
        new_list = List.objects.get()
        self.assertRedirects(response,f'/lists/{new_list.id}/')

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={"item_text":"A new item for existing list"}
        )

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={"item_text":"A new item for existing list"}
        )
        
        self.assertRedirects(response, f'/lists/{correct_list.id}/')




   
        













