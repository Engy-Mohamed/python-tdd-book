from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError



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



    def test_cannot_save_empty_list_items(self):

        list_ = List.objects.create()
        item = Item(list=list_,text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
    
        













