from django.shortcuts import render, redirect
from .models import *
from django.forms import inlineformset_factory
from .forms import OrderForm
from .filters import OrderFilter


# Create your views here.
def dashboard(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    latest_orders = orders.order_by('-date_created')[:5]
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    context = {
        "customers" : customers,
        "orders" : orders,
        "latest_orders": latest_orders,
        "total_orders" : total_orders,
        "orders_delivered" : orders_delivered,
        "orders_pending" : orders_pending,
    }
    return render(request, "crm/dashboard.html", context)

def products(request):
    products = Product.objects.all()
    context = {
        "products" : products,
    }
    return render(request, "crm/products.html", context)
                  
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    myFilter = OrderFilter(request.GET, orders)
    orders = myFilter.qs
    context = {
        "customer" : customer,
        "orders" : orders,
        "myFilter" : myFilter,
    }
    return render(request, "crm/customer.html", context)

def create_order(request, pk):
    customer = Customer.objects.get(id=pk)
    OrderFormset = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=4)
    formset = OrderFormset(instance=customer)
    
    if request.method == "POST":
        formset = OrderFormset(request.POST, instance=customer)
        if formset.is_valid:
            formset.save()
            return redirect('dashboard')
    context = {
        "formset": formset,
    }
    return render(request, 'crm/order_form.html', context)
        
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid:
            form.save()
            return redirect('dashboard')
    context = {
        'form': form,
    }
    return render(request, 'crm/order_form.html', context)

def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('dashboard')
    context = {
        "order":order,
    }
    return render(request, 'crm/delete_order.html', context)