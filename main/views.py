from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from .models import *
from django.shortcuts import redirect
from .forms import LostsalesForm
from django.forms import inlineformset_factory
from .filters import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages, humanize
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


@login_required()
def allcaptures(request):

    lostsales = Lostsales.objects.filter(
        user=request.user).order_by('-created_date')
    # if 'term' in request.GET:
    #     prod = Products.objects.filter(
    #         description__icontains=request.GET.get('term'))
    #     for i in prod:
    #         data.append(i.description)

    #     return JsonResponse(data, safe=False)
    # formset = inlineformset_factory()

    myFilter = lostSalesFilter(request.GET, queryset=lostsales)
    # myFilter = productFilter(request.GET, queryset=allprod)

    if request.method == 'GET':
        lostsales = myFilter.qs

    context = {'lostsales': lostsales,
               'myfilter': myFilter,


               }

    return render(request, 'main/home.html', context)


@login_required()
def item_select(request):
    b = Products.objects.all().order_by('description')
    prod = Products.objects.none()
    lostsales = Lostsales.objects.filter(user=request.user.id)

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
               lostsales: lostsales,
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

    context = {}

    return render(request, 'main/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


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
            staff.branch = Stores(request.POST.get('branch'))
            if staff.branch == 'Back Office':
                group = Group.objects.get(name='BackOffice')
            elif staff.branch == 'Retail Ops':
                group = Group.objects.get(name='RetailOps')
            else:
                group = Group.objects.get(name='Branch')
            user.groups.set([group])
            staff.save()
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
        form = LostsalesForm(instance=item)
        formitem = {
            'upc': item.upc,
            'description': item.description,
            'attributes': item.attributes,
            'size': item.size,
            'id': item.id,
        }

        return JsonResponse(formitem, safe=False)
        # Below code is for normal html page
        # return render(request, 'main/additem.html', formitem)

    return redirect('home')


def capture(request):  # Model that saves the lost sales
    if request.method == 'POST':
        print(request.user.staff)
        item = request.POST.get('product')
        product = Products.objects.get(id=item)
        lost = Lostsales()
        lost.product = product
        lost.quantity = request.POST.get('quantity')
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
