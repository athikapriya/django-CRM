from django.shortcuts import render


# homepage view
def homepage(request):
    context = {}
    return render(request, 'base/homepage.html', context)



# products view
def products(request):
    context = {}
    return render(request, 'base/products.html', context)



# customer view
def customer(request):
    context = {}
    return render(request, 'base/customer.html', context)