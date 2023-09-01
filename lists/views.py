from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError

# Create your views here.
def home_page(request):

    #render  auto searchs  folders called templates inside any apps'directorires
    #then build httpResponce
    # dic.get to get default value when we make get request
    """     return render(
        request,
        "home.html",
        {"new_item_text" : request.POST.get("item_text","")}
    ) """
    # get method
    return render(request,"home.html")

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST["item_text"], list=list_)
            item.full_clean()
            item.save()
            return redirect(f"/lists/{list_.id}/")
        except ValidationError:
            error = "You can't add an empty list item"
    return render(request,"list.html", {"list" : list_,"error":error})

def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST["item_text"], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't add an empty list item"
        return render(request, 'home.html',{"error":error})
    return redirect(f"/lists/{list_.id}/")

