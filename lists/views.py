from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from lists.forms import ItemForm
from lists.models import Item, List

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
    return render(request,"home.html", {'form' : ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
  
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list= list_)
            return redirect(list_)
        
    return render(request,"list.html", 
                  {"list" : list_, "form" : form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list= list_)
        return redirect(list_)
    else:
        return render(request, 'home.html',{"form":form})
        

