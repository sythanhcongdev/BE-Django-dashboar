from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt, csrf_protect


urlpatterns = [
    path('', views.index, name="expenses"),
    path('add-expenses', views.add_expenses, name="add-expenses"),
    path('expense-edit/<int:id>', views.expense_edit, name="expense-edit"),
    path('expense-delete/<int:id>', views.expense_delete, name="expense-delete"),
    path('expense-search', csrf_exempt(views.search_expenses), name="expense-search"),
]
