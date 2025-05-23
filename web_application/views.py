from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Item, Receipt
from .serializers import CategorySerializer, ReceiptSerializer


def login_page(request):
    if request.user.is_authenticated:
        return redirect('receipts')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('receipts')
        else:
            messages.error(request, 'Invalid username or password!')
            return render(request, 'loginPage.html')
    return render(request, 'loginPage.html')


@login_required
def logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login_page')


@login_required
def receipts(request):
    all_receipts = Receipt.objects.all()
    all_categories = Category.objects.all()
    context = {
        'receipts': all_receipts,
        'categories': all_categories
    }
    return render(request, 'receipts.html', context)


@login_required
def add_receipt(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        if name and date:
            receipt = Receipt.objects.create(name=name, date=date)
            receipt_items_name = request.POST.getlist('receipt-items-name[]')
            receipt_items_price = request.POST.getlist('receipt-items-price[]')
            receipt_items_category = request.POST.getlist('receipt-items-category[]')
            for i in range(len(receipt_items_name)):
                category = Category.objects.get(pk=receipt_items_category[i]) if receipt_items_category[i] else None
                Item.objects.create(name=receipt_items_name[i],
                                    price=receipt_items_price[i],
                                    receipt=receipt,
                                    category=category)
            messages.success(request, 'Receipt added successfully!')
    return redirect('receipts')


@login_required
def edit_receipt(request, receipt_id):
    receipt = Receipt.objects.get(pk=receipt_id)
    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_date = request.POST.get('date')
        if new_name and new_date:
            receipt.name = new_name
            receipt.date = new_date
            receipt.save()
            receipt.items.all().delete()
            receipt_items_name = request.POST.getlist('receipt-items-name[]')
            receipt_items_price = request.POST.getlist('receipt-items-price[]')
            receipt_items_category = request.POST.getlist('receipt-items-category[]')
            for i in range(len(receipt_items_name)):
                category = Category.objects.get(pk=receipt_items_category[i]) if receipt_items_category[i] else None
                Item.objects.create(
                    name=receipt_items_name[i],
                    price=receipt_items_price[i],
                    receipt=receipt,
                    category=category
                )
            messages.success(request, 'Receipt edited successfully!')
    return redirect('receipts')


@login_required
def delete_receipt(request, receipt_id):
    receipt = Receipt.objects.get(pk=receipt_id)
    if request.method == 'POST':
        receipt.delete()
        messages.success(request, 'Receipt deleted successfully!')
    return redirect('receipts')


@login_required
@api_view(['GET'])
def receipts_list(request):
    all_receipts = Receipt.objects.all()
    serializer = ReceiptSerializer(all_receipts, many=True)
    return Response(serializer.data)


@login_required
@api_view(['GET'])
def receipt_details(request, receipt_id):
    try:
        receipt = Receipt.objects.get(pk=receipt_id)
    except Receipt.DoesNotExist:
        return Response({'error': 'Receipt not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ReceiptSerializer(receipt)
    return Response(serializer.data)


@login_required
def categories(request):
    all_categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': all_categories})


@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, 'Category added successfully!')
    return redirect('categories')


@login_required
def edit_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name:
            category.name = new_name
            category.save()
            messages.success(request, 'Category edited successfully!')
    return redirect('categories')


@login_required
def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
    return redirect('categories')


@login_required
@api_view(['GET'])
def categories_list(request):
    all_categories = Category.objects.all()
    serializer = CategorySerializer(all_categories, many=True)
    return Response(serializer.data)


@login_required
@api_view(['GET'])
def category_details(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found!'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CategorySerializer(category)
    return Response(serializer.data)


@login_required
def expense_report(request):
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    expenses = {}
    if start_date and end_date:
        all_categories = Category.objects.all()
        for category in all_categories:
            category_items = Item.objects.filter(category=category, receipt__date__range=[start_date, end_date])
            category_expenses = category_items.aggregate(expenses=Sum('price'))['expenses'] or 0
            expenses[category.name] = f"{category_expenses:.2f}"
        uncategorized_category_items = Item.objects.filter(category=None, receipt__date__range=[start_date, end_date])
        uncategorized_expenses = uncategorized_category_items.aggregate(expenses=Sum('price'))['expenses'] or 0
        expenses['N/A'] = f"{uncategorized_expenses:.2f}"
        messages.success(request, 'Expense report generated successfully!')
    context = {
        'start_date': datetime.strptime(start_date, '%Y-%m-%d').strftime('%d.%m.%Y') if start_date else None,
        'end_date': datetime.strptime(end_date, '%Y-%m-%d').strftime('%d.%m.%Y') if end_date else None,
        'expenses': expenses if expenses else None,
    }
    return render(request, 'expenseReport.html', context)


@login_required
def settings(request):
    return render(request, 'settings.html')
