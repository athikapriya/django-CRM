from django.shortcuts import render
from .models import *


# homepage view
def homepage(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    total_pending = orders.filter(status="Pending").count()
    total_delivered = orders.filter(status="Delivered").count()
    context = {
        "total_orders" : total_orders,
        "total_pending" : total_pending,
        "total_delivered" : total_delivered
    }
    return render(request, 'base/homepage.html', context)



# products view
def products(request):
    context = {}
    return render(request, 'base/products.html', context)



# customer view
def customer(request):
    context = {}
    return render(request, 'base/customer.html', context)