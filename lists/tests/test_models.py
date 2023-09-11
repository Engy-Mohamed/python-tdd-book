from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError



class ListAndItemModelsTest(TestCase):

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
    
    def test_duplicate_items_are_invalid(self):

        list_ = List.objects.create()
        Item.objects.create(list=list_, text='add salt')
        with self.assertRaises(IntegrityError):
            item = Item.objects.create(list=list_, text='add salt')
            #item.full_clean()
            item.save()

    def test_CAN_save_same_item_to_different_lists(self):

        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='add salt')
        item = Item(list=list2, text='add salt')
        item.full_clean() #should not raise

    def test_list_ordering(self):

        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text="add salt")
        self.assertEqual(str(item), "add salt")

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())


class ItemModelTest(TestCase):

    def test_default_text(self):
        item =Item()
        self.assertEqual(item.text, '')


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(),f'/lists/{list_.id}/')







