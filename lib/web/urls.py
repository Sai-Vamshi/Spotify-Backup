"""Is used to control all the urls caalled in the front-end of the application"""
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from .views import index, userdetails, delete_integration, view_integration
admin.autodiscover()
app_name = 'web'

urlpatterns = [

    # This returns all the integrations of a particular user
    path("user/", userdetails, name="home"),

    # For deleting a particular integration
    path("user/<int:id>", delete_integration, name="home"),

    # For viewing an particular Integration
    path("account/<int:id>", view_integration, name="home"),
    url(r"^(?P<path>.*)$", index, name="home"),
]
