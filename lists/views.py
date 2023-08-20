from django.shortcuts import render

# Create your views here.
def home_page(request):
    #render  auto searchs  folders called templates inside any apps'directorires
    #then build httpResponce
    return render(request,"home.html")