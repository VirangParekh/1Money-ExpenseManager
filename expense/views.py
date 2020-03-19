from urllib.parse import quote_plus
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import PostForm
from django.contrib.auth.models import User,auth
from .models import Expenditure,Customer,Income,Data
from django.db.models import Q
import itertools

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Successfully Created")
        return redirect("expense:timeline")
    context = {
        "form" : form,
        "action":"create",
    }
    return render(request, "post_form.html", context)

def post_detail(request,id):
    instance = get_object_or_404(Data, id=id)
    context = {
        "title": instance.sub_category, 
        "instance" : instance,
    }
    return render(request, "post_detail.html", context)

def timeline(request):
    queryset_list = Data.objects.filter(user=request.user)
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(sub_category__icontains=query)|
            Q(spent__icontains=query)

        ).distinct()
    paginator = Paginator(queryset_list, 5) # Show 5 contacts per page
    page_request_var ="page"
    page = request.GET.get(page_request_var)
    queryset = paginator.get_page(page)

    context = {
        "object_list" : queryset,
        "title": "Expenditures",
        "page_request_var": page_request_var, 
    }
    return render(request, "timeline.html", context)    

def post_update(request,id=None):
    instance = get_object_or_404(Data, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("expense:timeline")    
    context = {
        "title": instance.sub_category, 
        "instance" : instance,
        "action":"update",
        "form" : form,
    }
    return render(request, "post_form.html", context)


def post_delete(request,id=None):
    instance = get_object_or_404(Data, id=id)
    instance.delete()
    messages.success(request,"Successfully Deleted")
    return redirect("expense:timeline")

def analytics(request):
    dataset = Data.objects.filter(user=request.user)
    context = {
        "object_list" : dataset,
        "title" : "Expenditure",
    }
    
    return render(request, 'analytics.html', context) 
    
def budget(request):
    sub_cat = set(Data.objects.values_list('sub_category',flat="true").filter(user=request.user))
    cat = set(Expenditure.objects.values_list('category',flat="true"))
    context = {
        "object_list1" : sub_cat,
        "object_list2" : cat,
        "title1": "Sub Categories",
        "title2": "Categories",
#        "cat_dict":get_category_dict,
        }
    return render(request,'budget.html',context)

def get_category_dict(request):
    cat_dict=dict()
    categories=Expenditure.objects.all()
    for category in categories:
        l=[]
        subcategories=category.dataset.all()
        for subcategory in subcategories:
            l.append(subcategory.sub_category)
        cat_dict[category.category]=l