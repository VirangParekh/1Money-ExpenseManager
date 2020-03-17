#from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, include
from . import views
from expense import views as expense_views

app_name = 'expense'

urlpatterns = [
    path('sems/',views.sems, name='sems'),
    path('sems/post_create/',views.post_create, name="post_create"),
    path('sems/post_detail/<int:id>',views.post_detail, name="post_detail"),   
    path('sems/timeline/',views.timeline, name="timeline"),
    path('sems/post_update/<int:id>',views.post_update, name="post_update"),
    path('sems/post_delete/<int:id>',views.post_delete, name="post_delete"),
    path('analytics/',views.analytics,name='analytics'),
]