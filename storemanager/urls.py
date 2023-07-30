"""storemanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from stock import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('dealer/',views.dealer,name='dealer'),
    path('sale-entry/',views.entryForm,name='entryForm'),
    path('dealer/<slug:slug>',views.dealer,name='dealer'),
    path('bill/',views.generateBill,name='bill'),
    path('bills/',views.createBill,name='createbill'),
    path('accounts/',views.updateAccounts,name='updateaccounts'),
    path('',views.homepage,name='homepage'),
    path('item/<str:name>',views.items,name='item-detail'),
]
