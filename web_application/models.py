from django.db import models
from django.db.models import Sum


class Item(models.Model):
    name = models.CharField(max_length=25, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    receipt = models.ForeignKey('Receipt', on_delete=models.CASCADE, related_name='items', blank=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='items', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'items'


class Category(models.Model):
    name = models.CharField(max_length=25, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Receipt(models.Model):
    name = models.CharField(max_length=25, blank=False)
    date = models.DateField(blank=False)

    def total_amount(self):
        total_amount = self.items.aggregate(total_amount=Sum('price'))['total_amount'] or 0
        return f'{total_amount:.2f}'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'receipts'
