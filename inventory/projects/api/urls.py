# -*- coding: utf-8 -*-
#
# inventory/projects/api/urls.py
#

from django.conf.urls import include, url

from inventory.projects.api import views


urlpatterns = [
    url(r'inventory-types$', views.inventory_type_list,
        name='inventory-type-list' ),
    url(r'inventory-types/(?P<public_id>\w+)/$', views.inventory_type_detail,
        name='inventory-type-detail'),
    #url(r'memberships$', views.membership_list, name='membership-list'),
    #url(r'memberships/(?P<pk>\d+)/$', views.membership_detail,
    #    name='membership-detail'),
    url(r'projects/$', views.project_list, name="project-list"),
    url(r'projects/(?P<public_id>\w+)/$', views.project_detail,
        name="project-detail"),
    ]
