"""
URL configuration for receiptly project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from web_application import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expense-report/', views.expense_report, name='expense_report'),
    path('receipts/', views.receipts, name='receipts'),
    path('add-receipt/', views.add_receipt, name="add_receipt"),
    path('edit-receipt/<int:receipt_id>/', views.edit_receipt, name='edit_receipt'),
    path('delete-receipt/<int:receipt_id>/', views.delete_receipt, name="delete_receipt"),
    path('api/receipts/', views.receipts_list, name='receipts_list'),
    path('api/receipts/<int:receipt_id>/', views.receipt_details, name='receipt_details'),
    path('categories/', views.categories, name='categories'),
    path('add-category/', views.add_category, name="add_category"),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('api/categories/', views.categories_list, name='categories_list'),
    path('api/categories/<int:category_id>/', views.category_details, name='category_details'),
    path('settings/', views.settings, name='settings'),
]
