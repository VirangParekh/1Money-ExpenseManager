from urllib.parse import quote_plus
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import PostForm
from django.contrib.auth.models import User,auth
from .models import Expenditure,Customer,Income
from django.db.models import Q

def sems(request):
    return render(request,'timeline.html')

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form" : form,
        "action":"create",
    }
    return render(request, "post_form.html", context)

def post_detail(request,id):
    instance = get_object_or_404(Expenditure, id=id)
    share_string = quote_plus(instance.content)
    context = {
        "title": instance.category, 
        "instance" : instance,
        "share_string" : share_string,
    }
    return render(request, "post_detail.html", context)

def timeline(request):
    queryset_list = Expenditure.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
            
        ).distinct()
    paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
    page_request_var ="page"
    page = request.GET.get(page_request_var)
    queryset = paginator.get_page(page)

    context = {
        "object_list" : queryset,
        "title": "List",
        "page_request_var": page_request_var, 
    }
    return render(request, "timeline.html", context)    

def post_update(request,id=None):
    instance = get_object_or_404(Expenditure, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    
    context = {
        "title": instance.category, 
        "instance" : instance,
        "action":"update",
        "form" : form,
    }
    return render(request, "post_form.html", context)


def post_delete(request,id=None):
    instance = get_object_or_404(Expenditure, id=id)
    instance.delete()
    messages.success(request,"Successfully Deleted")
    return redirect("expense:timeline")

def analytics(request):
    return render(request,'analytics.html') 
