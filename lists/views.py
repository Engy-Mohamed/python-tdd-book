from django.shortcuts import render, redirect
from lists.models import Item

# Create your views here.
def home_page(request):

    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect('/')

    #render  auto searchs  folders called templates inside any apps'directorires
    #then build httpResponce
    # dic.get to get default value when we make get request
    """     return render(
        request,
        "home.html",
        {"new_item_text" : request.POST.get("item_text","")}
    ) """
    items = Item.objects.all()

    return render(
        request,
        "home.html",
        {"items" : items}
    )