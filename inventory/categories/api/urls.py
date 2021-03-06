# -*- coding: utf-8 -*-
#
# inventory/categories/api/urls.py
#

from django.conf.urls import include, url

from .views import category_list, category_detail, category_clone


urlpatterns = [
    url(r'categories/$', category_list,
        name="category-list"),
    url(r'categories/(?P<public_id>\w+)/$', category_detail,
        name="category-detail"),
    url(r'category-clone/$', category_clone, name='category-clone'),
    ]
