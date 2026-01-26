from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm, RequestOTPForm, VerifyOTPForm, SetNewPasswordForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.core.paginator import Paginator
import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.mail import EmailMessage



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
                return redirect("user_profile", username=user.username)
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
                return redirect("user_profile", username = user.username)
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

    # customer paginator
    customer_list = Customer.objects.all().order_by("-id")
    customer_paginator = Paginator(customer_list, 5)
    customer_page_number = request.GET.get("customer_page")
    customers = customer_paginator.get_page(customer_page_number)

    # order paginator
    order_list = Order.objects.order_by("-date_created")
    order_paginator = Paginator(order_list, 5)
    order_page_number = request.GET.get("order_page")
    orders = order_paginator.get_page(order_page_number)

    total_orders = order_list.count()
    total_pending = order_list.filter(status="Pending").count()
    total_delivered = order_list.filter(status="Delivered").count()

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
def userProfile(request, username):

    if not User.objects.filter(username=username).exists():
        return redirect("unauthorized")
    
    if request.user.username != username:
        return redirect("unauthorized")
    
    customer = request.user.customer
    orders = customer.order_set.all()

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



# account settings view
@login_required(login_url="login")
@allowed_users(['customer'])
def accountSettings(request, username):

    if request.user.username != username :
        return redirect("unauthorized")
    
    customer = request.user.customer

    if request.method == "POST":
        print(request.FILES)
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("user_profile", username=request.user.username)
    else:
        form = CustomerForm(instance=customer)

    context = {
        "form": form,
        "customer": customer
    }
    return render(request, "base/account_settings.html", context)



# password recovery choice vews
def password_recovery_choice(request):
    context = {}
    return render(request, 'base/password_recovery_choice.html', context)



# request password views
def request_password_otp(request):
    if request.method == "POST":
        form = RequestOTPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                # Check if user exists
                user = User.objects.get(email=email)

                # Generate OTP
                otp = str(random.randint(100000, 999999))
                PasswordResetOTP.objects.create(user=user, otp=otp)

                # email body
                email_body = f"""
ClientHub Security Team 🔐

Your One-Time Password (OTP):
{otp}

⏳ Expires in 6 minutes

If you didn’t request this, ignore this email.
 — ClientHub
"""

                # Send email
                email_msg = EmailMessage(
                    subject="ClientHub Password Reset OTP",
                    body=email_body,
                    from_email="ClientHub Security Team <yourgmail@gmail.com>",
                    to=[email],
                )
                email_msg.send()

                # Save user ID in session for verification
                request.session['reset_user_id'] = user.id
                messages.success(request, "OTP sent to your email!")
                return redirect("verify_otp")

            except User.DoesNotExist:
                messages.error(request, "No user found with this email")
    else:
        form = RequestOTPForm()

    return render(request, "base/request_otp.html", {"form": form})



# verify OTP view
def verify_otp(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, "Session expired. Please enter your email again.")
        return redirect("password_reset_otp")
    
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp_input = form.cleaned_data['otp']

            otp_record = PasswordResetOTP.objects.filter(
                user=user,
                otp=otp_input,
                is_used=False
            ).last()

            if otp_record and otp_record.is_valid():
                otp_record.is_used = True   
                otp_record.save()

                request.session['otp_verified'] = True 
                return redirect("password_reset_now")
            else:
                form.add_error('otp', "Invalid or expired OTP")  
    else:
        form = VerifyOTPForm()

    return render(request, "base/verify_otp.html", {"form": form})



# password reset now views
def password_reset_now(request):
    user_id = request.session.get('reset_user_id')
    otp_verified = request.session.get('otp_verified', False)

    if not user_id or not otp_verified:
        messages.error(request, "Unauthorized access.")
        return redirect("request_password_otp")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()

            del request.session['reset_user_id']
            del request.session['otp_verified']

            messages.success(request, "Password reset successfully! Please login.")
            return redirect("login")
    else:
        form = SetNewPasswordForm()

    context = {
        "form": form
    }
    return render(request, "base/password_reset_now.html", context)




# products view
@login_required(login_url="login")
@allowed_users(['admin'])
def products(request):
    products_list = Product.objects.all().order_by('-id') 
    page_number = request.GET.get('page')  
    paginator = Paginator(products_list, 5) 
    products = paginator.get_page(page_number)

    context = {
        "products" : products
    }
    return render(request, 'base/products.html', context)



# customer view
@login_required(login_url="login")
@allowed_users(['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    
    order_list = customer.order_set.order_by("-date_created")
   
    myFilter = OrderFilter(request.GET, queryset=order_list)
    filtered_orders = myFilter.qs

    page_number = request.GET.get("order_page")
    paginator = Paginator(filtered_orders, 5) 
    orders = paginator.get_page(page_number)

    total_order = order_list.count()
    
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