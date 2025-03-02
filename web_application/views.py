from datetime import datetime

from django.db.models import Sum
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import CategorySerializer
from .serializers import ReceiptSerializer
from .models import Item
from .models import Receipt
from .models import Category


def receipts(request):
    all_receipts = Receipt.objects.all()
    all_categories = Category.objects.all()
    context = {
        'receipts': all_receipts,
        'categories': all_categories
    }
    return render(request, 'receipts.html', context)


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


def delete_receipt(request, receipt_id):
    receipt = Receipt.objects.get(pk=receipt_id)
    if request.method == 'POST':
        receipt.delete()
        messages.success(request, 'Receipt deleted successfully!')
    return redirect('receipts')


@api_view(['GET'])
def receipts_list(request):
    all_receipts = Receipt.objects.all()
    serializer = ReceiptSerializer(all_receipts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def receipt_details(request, receipt_id):
    try:
        receipt = Receipt.objects.get(pk=receipt_id)
    except Receipt.DoesNotExist:
        return Response({'error': 'Receipt not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ReceiptSerializer(receipt)
    return Response(serializer.data)


def categories(request):
    all_categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': all_categories})


def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, 'Category added successfully!')
    return redirect('categories')


def edit_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name:
            category.name = new_name
            category.save()
            messages.success(request, 'Category edited successfully!')
    return redirect('categories')


def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
    return redirect('categories')


@api_view(['GET'])
def categories_list(request):
    all_categories = Category.objects.all()
    serializer = CategorySerializer(all_categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category_details(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found!'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CategorySerializer(category)
    return Response(serializer.data)


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


def settings(request):
    return render(request, 'settings.html')
