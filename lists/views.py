from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):

    #render  auto searchs  folders called templates inside any apps'directorires
    #then build httpResponce
    # dic.get to get default value when we make get request
    return render(
        request,
        "home.html",
        {"new_item_text" : request.POST.get("item_text","")}
    )