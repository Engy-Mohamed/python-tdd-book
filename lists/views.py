from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import Item, List
from django.contrib.auth import get_user_model
User = get_user_model()

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
    form = ExistingListItemForm(for_list=list_)
  
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
        
    return render(request,"list.html", 
                  

                  {"list" : list_, "form" : form})


def new_list(request):
    form = NewListForm(data=request.POST) 
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(str(list_.get_absolute_url()))
    return render(request, 'home.html', {'form': form})
      

def my_lists(request, email):
    owner = User.objects.get(email=email)
    shared_lists = List.objects.filter(shared_with=owner).all()
    return render(request, 'my_lists.html', {'owner': owner,'shared_lists':shared_lists })

def share_list(request, list_id):

    share_with_email = request.POST.get('share_email')
    list_ = List.objects.get(id=list_id)
    user_ = User.objects.get(email=share_with_email)
    list_.shared_with.add(user_)
    return redirect(list_)




