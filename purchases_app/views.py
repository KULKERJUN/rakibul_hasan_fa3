from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.db.models import Sum, Q
from django.contrib import messages
from purchases_app.models import *
from purchases_app.forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    form_data = AuthenticationForm()
    if request.method == 'POST':
        form_data = AuthenticationForm(request, data = request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            if user:
                login(request,user)
                return redirect('dashboard_view')

    context = {
        'title': 'LOGIN',
        'page_title': 'Please login with valid credentials',
        'form_btn': 'Login',
        'form_data': form_data,
    }

    return render(request,'master/baseform.html',context)

def register_view(request):
    form_data = RegistrationForm()
    if request.method == 'POST':
        form_data = RegistrationForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('login_view')

    context = {
            'title': 'REGISTER',
            'page_title': 'Please register with your credentials',
            'form_btn': 'Register',
            'form_data': form_data,
        }
    return render(request,'master/baseform.html',context)

@login_required
@login_required
def dashboard_view(request):
    purchases = PurchaseModel.objects.filter(user=request.user)

    total_subtotal = purchases.aggregate(total_subtotal=Sum('subtotal'))['total_subtotal'] or 0
    total_amount = purchases.aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0
    total_due = purchases.aggregate(total_due=Sum('due_amount'))['total_due'] or 0

    context = {
        'title': 'Dashboard',
        'total_subtotal': total_subtotal,
        'total_amount': total_amount,
        'total_due': total_due,
    }

    return render(request, 'dashboard.html', context)

@login_required
def profile_view(request):
    try:
        data = UserProfileModel.objects.get(user = request.user)
    except:
        data = None
        return redirect('update_profile_view')
    context = {'data':data,}
    return render(request, 'profile.html', context)

@login_required
def update_profile_view(request):
    try:
        data = UserProfileModel.objects.get(user = request.user)
    except:
        data = None
    form_data = UpdateProfileForm(instance = data)
    if request.method == 'POST':
        form_data = UpdateProfileForm(request.POST,request.FILES,instance = data)
        if form_data.is_valid():
            form_data = form_data.save(commit = False)
            form_data.user = request.user
            form_data.save()
            return redirect('profile_view')
    context = {
                'title': 'Update Profile',
                'page_title': 'Please update profile with your credentials',
                'form_btn': 'Update',
                'form_data': form_data,
            }

    return render(request,'master/baseform.html',context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')

#SUPPLIER
@login_required
def supplier_list_view(request):
    try:
        data = SupplierModel.objects.filter(user=request.user)
    except:
        data = None
        return redirect('supplier_add_view')
    data = SupplierModel.objects.filter(user= request.user)
    context={'title': 'Suppliers List Below:','data':data}
    return render(request,'suppliers.html',context)

@login_required
def supplier_add_view(request):
    form_data = SupplierForm()
    if request.method == 'POST':
        form_data = SupplierForm(request.POST)
        if form_data.is_valid():
            form_data = form_data.save(commit = False)
            form_data.user = request.user
            form_data.save()
            return redirect('supplier_list_view')
    context = {
                'title': 'Add Supplier',
                'page_title': 'Add Your Suppliers HERE !',
                'form_btn': 'ADD',
                'form_data': form_data,
            }
    
    return render(request,'master/baseform.html',context)

@login_required
def supplier_edit_view(request,id):
    data = get_object_or_404(SupplierModel, id = id)
    form_data = SupplierForm(instance = data)
    if request.method == 'POST':
        form_data = SupplierForm(request.POST,instance = data)
        if form_data.is_valid():
            form_data = form_data.save(commit = False)
            form_data.user = request.user
            form_data.save()
            return redirect('supplier_list_view')
    context = {
                'title': 'Update Supplier',
                'page_title': 'Please update Supplier with your credentials',
                'form_btn': 'Update',
                'form_data': form_data,
            }
    return render(request,'master/baseform.html',context)

@login_required
def supplier_delete_view(request,id):
    get_object_or_404(SupplierModel,id = id).delete()
    return redirect('supplier_list_view')

#purchase
@login_required
def purchase_list_view(request):
    try:
        data = PurchaseModel.objects.filter(user=request.user)
    except:
        data = None
        return redirect('purchase_add_view')
    data = PurchaseModel.objects.filter(user= request.user)
    search_data = request.GET.get('search_data')
    if search_data:
        data = PurchaseModel.objects.filter(
            Q(user= request.user)& 
            Q(product_name__icontains=search_data)|
            Q(supplier__supplier_name__icontains=search_data))
    context={'title': 'Purchase List Below:','data':data}
    return render(request,'purchase.html',context)

@login_required
def purchase_add_view(request):
    form_data = PurchaseForm()
    if request.method == 'POST':
        form_data = PurchaseForm(request.POST)
        if form_data.is_valid():
            form_data = form_data.save(commit = False)
            form_data.user = request.user
            form_data.subtotal = form_data.quantity * form_data.unit_price
            form_data.total_amount = form_data.subtotal - form_data.discount
            form_data.due_amount = form_data.total_amount * form_data.paid_amount
            form_data.save()
            return redirect('purchase_list_view')
    context = {
                'title': 'Add Purchase',
                'page_title': 'Add Your Purchases HERE !',
                'form_btn': 'ADD',
                'form_data': form_data,
            }
    
    return render(request,'master/baseform.html',context)

@login_required
def purchase_edit_view(request,id):
    data = get_object_or_404(PurchaseModel, id = id)
    form_data = PurchaseForm(instance = data)
    if request.method == 'POST':
        form_data = PurchaseForm(request.POST,instance = data)
        if form_data.is_valid():
            form_data = form_data.save(commit = False)
            form_data.user = request.user
            form_data.save()
            return redirect('purchase_list_view')
    context = {
                'title': 'Update Purchase',
                'page_title': 'Please update Purchase with your credentials',
                'form_btn': 'Update',
                'form_data': form_data,
            }
    return render(request,'master/baseform.html',context)

@login_required
def purchase_delete_view(request,id):
    get_object_or_404(PurchaseModel,id = id).delete()
    return redirect('purchase_list_view')