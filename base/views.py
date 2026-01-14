from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only



# register page views
@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("user")
            
            messages.success(request, "Account created successfully. Welcome {username}" )
            return redirect("login")

    context= {
        "form" : form
    }
    return render(request, 'base/register.html', context)



# login page views
@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser or user.groups.filter(name="admin").exists():
                return redirect("homepage")
            elif user.groups.filter(name="customer").exists():
                return redirect("user")
            else:
                return redirect("unauthorized")
            
        else:
            messages.info(request, "Username or password is incorrect !")
    context = {
        
        }
    return render(request, 'base/login.html', context)



# logout view
def logoutUser(request):
    logout(request)
    return redirect("login")



# unauthorized user
def unauthorized(request):
    context = {

    }
    return render(request, "base/unauthorized.html", context)



# homepage view
@login_required(login_url="login")
@admin_only
def homepage(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    total_pending = orders.filter(status="Pending").count()
    total_delivered = orders.filter(status="Delivered").count()

    can_view_dashboard = (
        request.user.is_superuser or 
        request.user.groups.filter(name="admin").exists()
    )

    context = {
        "customers" : customers,
        "orders" : orders,
        "total_orders" : total_orders,
        "total_pending" : total_pending,
        "total_delivered" : total_delivered,
        "can_view_dashboard" : can_view_dashboard
    }
    return render(request, 'base/homepage.html', context)


    
# user profile view
@login_required(login_url="login")
@allowed_users(['customer'])
def userProfile(request):

    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    total_pending = orders.filter(status="Pending").count()
    total_delivered = orders.filter(status="Delivered").count()
    context = {
        "orders" : orders,
        "total_orders" : total_orders,
        "total_pending" : total_pending,
        "total_delivered" : total_delivered
    }
    return render(request, 'base/user_profile.html', context)



# products view
@login_required(login_url="login")
@allowed_users(['admin'])
def products(request):
    products = Product.objects.filter()
    context = {
        "products" : products
    }
    return render(request, 'base/products.html', context)



# customer view
@login_required(login_url="login")
@allowed_users(['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_order = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    
    context = {
        "customer" : customer,
        "orders" : orders,
        "total_order" : total_order,
        "myFilter" : myFilter
    }
    return render(request, 'base/customer.html', context)




# createOrder View
@login_required(login_url="login")
@allowed_users(['admin'])
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
@login_required(login_url="login")
@allowed_users(['admin'])
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
@login_required(login_url="login")
@allowed_users(['admin'])
def DeleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    next_url = request.GET.get("next", "/")

    if request.method == "POST":
        order.delete()
        return redirect(next_url)
    
    context = {
        "order" : order
    }
    return render(request, 'base/delete_order.html', context)