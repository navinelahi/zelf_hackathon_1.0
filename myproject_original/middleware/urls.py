from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^api/content/pages/(?P<page_no>[a-zA-Z0-9_-]+)/stat', views.get_content_list_with_stat),
    url(r'^api/content/pages/(?P<page_no>[a-zA-Z0-9_-]+)', views.get_content_list),
]
