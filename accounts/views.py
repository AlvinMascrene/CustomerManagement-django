from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory
# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customers.objects.all()
    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {
        'orders' : orders, 
        'customers' : customers, 
        'total_customers' : total_customers,
        'total_orders' : total_orders,
        'pending' : pending,
        'delivered' : delivered,
        }

    return render(request, 'accounts/dashboard.html', context)

def contact(request):
    return render(request, 'accounts/about.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

def customers(request, pk_test):
    customer = Customers.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_orders = orders.count()
    context = {
        'customer' : customer,
        'orders' : orders,
        'total_orders' : total_orders,
        }
    return render(request, 'accounts/customers.html',  context)

def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customers, Order, fields=('product', 'status'), extra=3)
    customer = Customers.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form  = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        # print('POST data : {}'.format(request.POST))
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset' : formset}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form' : form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST' :
        order.delete()
        return redirect('/')
    context = {'item' : order}
    return render(request, 'accounts/delete_order.html', context)
    