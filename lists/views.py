from django.shortcuts import render, redirect
from lists.models import Item

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

def view_list(request):
    items = Item.objects.all()
    return render(request,"list.html", {"items" : items})

def new_list(request):
    Item.objects.create(text=request.POST["item_text"])
    return redirect("/lists/the-only_list_in_the_world/")