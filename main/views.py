from django.shortcuts import render
import json
import csv
from django.http import HttpResponse, JsonResponse
from .models import *
from django.shortcuts import redirect
from .forms import LostsalesForm,  ProductForm
from django.forms import inlineformset_factory
from .filters import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages, humanize
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.db.models.query import EmptyQuerySet
from django.db.models import F, ExpressionWrapper, FloatField
import datetime
from django.utils import timezone
from django.views.generic import CreateView

# Create your views here.


@login_required()
def allcaptures(request):

    branch = str(request.user.groups.all()[0])

    if branch == 'BackOffice' or branch == 'RetailOps':

        lostsales = Lostsales.objects.all().order_by('-created_date')
    else:
        lostsales = Lostsales.objects.filter(
            store=request.user.staff.branch).order_by('-created_date')

    # if 'term' in request.GET:
    #     prod = Products.objects.filter(
    #         description__icontains=request.GET.get('term'))
    #     for i in prod:
    #         data.append(i.description)

    #     return JsonResponse(data, safe=False)
    # formset = inlineformset_factory()

    #myFilter = lostSalesFilter(request.GET, queryset=lostsales)
    # myFilter = productFilter(request.GET, queryset=allprod)
    if not request.GET.get('submit'):
        today = timezone.now()
        enddate = today + datetime.timedelta(days=1)

        startdate = today - datetime.timedelta(hours=today.hour)

        lostsales = lostsales.filter(
            created_date__gt=startdate, created_date__lt=enddate).order_by('-created_date')
    if request.method == 'GET':
        if request.GET.get('submit') == 'filter':
            if request.GET.get('start_date') == '' or request.GET.get('start_date') == '':
                today = timezone.now()
                enddate = today + datetime.timedelta(days=1)
                #enddate = enddate.date()

                startdate = today - datetime.timedelta(hours=today.hour)

            else:

                #lostsales = myFilter.qs
                enddate = request.GET.get('end_date')
                enddate = datetime.datetime.strptime(
                    enddate, '%Y-%m-%d') + datetime.timedelta(days=1)

                startdate = request.GET.get('start_date')
            lostsales = lostsales.filter(
                created_date__gt=startdate, created_date__lt=enddate)

        elif request.GET.get('submit') == 'export':
            if request.GET.get('start_date') == '' or request.GET.get('start_date') == '':
                message = "Date fields cannot be empty for export. Please enter a date range to export"
                messages.error(request, message)
                return redirect('home')
            response = HttpResponse(content_type='text/csv')

            enddate = request.GET.get('end_date')
            enddate = datetime.datetime.strptime(
                enddate, '%Y-%m-%d') + datetime.timedelta(days=1)

            startdate = request.GET.get('start_date')
            writer = csv.writer(response)
            writer.writerow(['UPC', 'ALU', 'Description1',
                             'Attributes', 'Size', 'Quantity', 'Price', 'Ext Price', 'Created_by', 'Branch', 'Date_created'])
            data = lostsales.filter(created_date__gt=startdate, created_date__lt=enddate).values_list(
                'product__upc', 'product__alu', 'product__description', 'product__attributes', 'product__size', 'quantity', 'product__price', ExpressionWrapper(F('quantity')*F('product__price'), output_field=FloatField()), 'user__username', 'store__name', 'created_date')

            for item in data:
                writer.writerow(item)
            response['content-disposition'] = 'attachment; filename="lostsales.csv'
            return response

    totalScan = lostsales.count()
    qty = 0
    extprice = 0
    for i in lostsales:
        qty = qty+i.quantity
        extprice = extprice+(i.quantity*i.product.price)

    context = {'lostsales': lostsales,

               'branch': branch,
               'totalcapture': totalScan,
               'quantity': qty,
               'extprice': extprice,



               }

    return render(request, 'main/home.html', context)


@login_required()
def item_select(request):
    b = Products.objects.all().order_by('description')
    prod = Products.objects.none()
    #lostsales = Lostsales.objects.filter(user=request.user.id)

    # if 'term' in request.GET:
    #     prod = Products.objects.filter(
    #         description__icontains=request.GET.get('term'))
    #     for i in prod:
    #         data.append(i.description)

    #     return JsonResponse(data, safe=False)

    if request.method == 'GET' and request.GET.get('description') is not None:
        myFilter = productFilter(request.GET, queryset=b)
        prod = myFilter.qs
    else:
        myFilter = productFilter(request.GET, queryset=prod)
        prod = Products.objects.none()

    context = {'prod': prod,
               'myfilter': myFilter,
               # lostsales: lostsales,
               }

    return render(request, 'main/home_branch.html', context)


def addlostsales(request):  # Old Function that was not used. Uses autocomplete
    prod = None
    data = []

    if 'term' in request.GET:
        prod = Products.objects.filter(
            description__icontains=request.GET.get('term'))
        for i in prod:
            data.append(i.description)

        return JsonResponse(data, safe=False)
    if request.method == 'POST':
        form = LostsalesForm()
        print(request.POST.get('product'))
    return redirect('home')


def loginUser(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            message = "Username or password Incorrect. Please confirm and try again"
            messages.warning(request, message)
            return redirect('login')

    context = {}

    return render(request, 'main/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@user_passes_test(lambda u: u.is_superuser)
def registerUser(request):
    if request.POST:

        content = {

            'username': request.POST.get('username'),
            'password1': request.POST.get('password1'),
            'password2': request.POST.get('password2'),
        }
        # print(content['password'])
        # return HttpResponse("died")
        staff = Staff()

        userform = UserCreationForm(content)

        if userform.is_valid():
            user = userform.save(commit=False)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()

            staff.user = user
            staff.branch = Stores.objects.get(id=(request.POST.get('branch')))

            staff.save()
            print(user.staff.branch, ' -branch')

            if str(staff.branch) == 'Back Office':
                group = Group.objects.get(name='BackOffice')

            elif str(staff.branch) == 'Retail Ops':
                group = Group.objects.get(name='RetailOps')
            else:
                group = Group.objects.get(name='Branch')

            user.groups.set([group])
            # staff.save()
            message = 'User {} Created Successfully. Please log in'.format(
                user)

            messages.success(
                request, message)
            return redirect('login')
        else:
            messages.error(request, userform.errors)
            return redirect('register')

    stores = Stores.objects.all().order_by('name')
    context = {
        'stores': stores
    }
    return render(request, 'main/register.html', context)


def additem(request):  # Function that shows where users can enter quantity

    if request.method == 'POST':

        # print(type(request.POST.get('id')))
        id = int(request.POST.get('id'))
        item = Products.objects.get(id=id)
        # print("________________________________________")
        # print(item)
        #form = LostsalesForm(instance=item)
        formitem = {
            'upc': item.upc,
            'description': item.description,
            'attributes': item.attributes,
            'size': item.size,
            'id': item.id,
            'price': item.price,
        }

        return JsonResponse(formitem, safe=False)
        # Below code is for normal html page
        # return render(request, 'main/additem.html', formitem)

    return redirect('home')


def edititem(request):  # Function that shows where users can enter quantity

    if request.method == 'POST':

        # print(type(request.POST.get('id')))
        id = int(request.POST.get('id'))
        item = Products.objects.get(id=id)

        #form = LostsalesForm(instance=item)
        formitem = {
            'upc': item.upc,
            'description': item.description,
            'attributes': item.attributes,
            'size': item.size,
            'id': item.id,
            'price': item.price,
        }

        return JsonResponse(formitem, safe=False)
        # Below code is for normal html page
        # return render(request, 'main/additem.html', formitem)

    return redirect('home')

# Change the price of an item.


def edit_price(request):
    if request.method == 'POST':
        id = request.POST.get('product')
        price = request.POST.get('price')
        item = Products.objects.get(id=id)
        print(item.price, '=old price')
        item.price = price
        print(item.price, 'new price')
        item.save()
        message = 'Price for {} changed successfully'.format(item.description)
        messages.success(request, message)

    return redirect('update_product')

# Add new product to the db


def create_item(request):
    if request.method == 'GET':
        return render(request, 'main/products_form.html')

    if request.method == 'POST':
        # print(request.POST)
        item = ProductForm(request.POST)
        item.is_bound
        item.save()

        return redirect('add_product')


def capture(request):  # Model that saves the lost sales
    if request.method == 'POST':

        item = request.POST.get('product')
        product = Products.objects.get(id=item)
        lost = Lostsales()
        lost.product = product
        qty = request.POST.get('quantity')
        lost.quantity = qty if qty else 1
        lost.store = request.user.staff.branch
        lost.user = User.objects.get(id=request.user.id)

        lost.save()
        messages.success(request, "Lost Sales Captured Successfully")

        # form = LostsalesForm(request.POST)
        # if form.is_valid():
        #     form.save(commit=False)
        #     print(form)
        # form.save(commit=False)
        # form.product = request.POST.get('product')
        # form.user = request.user.id
        # form.save()

        # print(form)

    return redirect('home')


@login_required()
def product_select(request):
    b = Products.objects.all().order_by('description')
    prod = Products.objects.none()

    if request.method == 'GET' and request.GET.get('description') is not None:
        myFilter = productFilter(request.GET, queryset=b)
        prod = myFilter.qs
    else:
        myFilter = productFilter(request.GET, queryset=prod)
        prod = Products.objects.none()

    context = {'prod': prod,
               'myfilter': myFilter,
               # lostsales: lostsales,
               }

    return render(request, 'main/product_list.html', context)
