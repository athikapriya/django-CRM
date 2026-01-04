from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory


# homepage view
def homepage(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    total_pending = orders.filter(status="Pending").count()
    total_delivered = orders.filter(status="Delivered").count()
    context = {
        "customers" : customers,
        "orders" : orders,
        "total_orders" : total_orders,
        "total_pending" : total_pending,
        "total_delivered" : total_delivered
    }
    return render(request, 'base/homepage.html', context)



# products view
def products(request):
    products = Product.objects.filter()
    context = {
        "products" : products
    }
    return render(request, 'base/products.html', context)



# customer view
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_order = orders.count()
    context = {
        "customer" : customer,
        "orders" : orders,
        "total_order" : total_order
    }
    return render(request, 'base/customer.html', context)




# createOrder View
def CreateOrder(request, pk):

    OrderFormSet = inlineformset_factory(Customer, Order, form=OrderForm, fields=("product", 'status', 'note'), extra=4)

    customer = Customer.objects.get(id=pk)
    formSet = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    next_url = request.GET.get("next", "/")

    if request.method == "POST":
        formSet = OrderFormSet(request.POST, instance=customer)
        if formSet.is_valid():
            formSet.save()
            return redirect(next_url)
        
    context = {
        "formSet" : formSet
    }
    return render(request, 'base/create_order.html', context)



# updateOrder Views
def UpdateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    next_url = request.GET.get("next", "/")

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect(next_url)
        
    context = {
        "form" : form,
        "order" : order
    }
    return render(request, "base/update_order.html", context)



# deleteOrder Views
def DeleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    next_url = request.GET.get("next", "/")

    if request.method == "POST":
        order.delete()
        return redirect(next_url)
    
    context = {
        "order" : order
    }
    return render(request, 'base/delete.html', context)