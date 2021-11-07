from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expenses
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
# Create your views here.
import json
from django.http import JsonResponse
from userpreferences.models import Userpreferences

def search_expenses(request):
    if request.method == 'POST':
        search_string = json.loads(request.body).get('searchText')
        expenses = Expenses.objects.filter(
            amount__istartswith=search_string, owner=request.user) | Expenses.objects.filter(
            date__istartswith=search_string, owner=request.user) | Expenses.objects.filter(
            description__icontains=search_string, owner=request.user) | Expenses.objects.filter(
            category__icontains=search_string, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expenses.objects.filter(owner=request.user)
    paginator=Paginator(expenses, 4)
    page_number=request.GET.get('page')
    page_obj=Paginator.get_page(paginator,page_number)
    currency = Userpreferences.objects.get(user=request.user).currency

    context ={
        'expenses':expenses,
        'page_obj':page_obj,
        'currency': currency,
    }

    return render(request, 'expenses/index.html', context)


def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expenses.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, ' Amount is required')
            return render(request, 'expenses/add_expenses.html', context)

        description = request.POST['description']
        date = request.POST['expenses_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expenses.html', context)

        Expenses.objects.create(owner=request.user, amount=amount, description=description, category=category, date=date)
        messages.success(request, 'Expenses saved successfully')

        return redirect('expenses')


def expense_edit(request, id):
    categories = Category.objects.all()
    expense = Expenses.objects.get(pk=id)
    context={
        'categories': categories,
        'expense' : expense,
        'values': expense,
    }
    if request.method == 'GET':
        return render(request, 'expenses/expense-edit.html',context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, ' Amount is required')
            return render(request, 'expenses/expense-edit.html', context)

        description = request.POST['description']
        date = request.POST['expenses_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/expense-edit.html', context)

        Expenses.objects.create(owner=request.user, amount=amount, description=description, category=category, date=date)
        
        expense.owner = request.user
        expense.amount=amount
        expense.description=description
        expense.category=category
        expense.date=date

        expense.save()

        messages.success(request, 'Expenses Updated successfully')        
        return redirect('expenses')

def expense_delete(request, id):
    expense =Expenses.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expenses deleted successfully')
    return redirect('expenses')
