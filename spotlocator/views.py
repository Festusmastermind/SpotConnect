from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from spotlocator.models import format_phone_number
from django.contrib.auth import get_user_model
from spotlocator.models import MenuList
from spotlocator.forms import OwnerProfileForm, MenuCreateForm
from django.db.models import Q
from validate_email import validate_email

User = get_user_model()


# Create your views here.

def register(request):
    # if the request is post
    if request.method == 'POST':
        context = {}
        template_name = 'spotlocator/user_register.html'
        user = User()
        if User.objects.filter(email=request.POST.get('email')).exists():
            messages.warning(request, f'Email already exists')
            return render(request, template_name, context)
        if not validate_email(request.POST.get('email')):
            messages.warning(request, f'Email is not Valid')
            return render(request, template_name, context)
        number = request.POST.get('number', None)
        if number:
            number = format_phone_number(number)
            if not number:
                messages.warning(request, f'Invalid Phone number')
                return render(request, template_name, context)
        else:
            messages.warning(request, f'Phone number is required')
            return render(request, template_name, context)
        if User.objects.filter(number=number).exists():
            messages.warning(request, f'Contact number already exists')
            return render(request, template_name, context)
         # receving the values
        user_type = request.POST.get('type')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        spotname = request.POST.get('spotname')
        spotlocation = request.POST.get('spotlocation')
        if user_type == 'customer':
            if firstname and lastname is None:
                messages.warning(request, f'First and lastname is required')
                return render(request, template_name, context)
            user.first_name = firstname
            user.last_name = lastname
            user.user_type = 1
        elif user_type == 'spotowner':
            if spotname and spotlocation is None:
                messages.warning(request, f'Spotname and SpotLocation is required')
                return render(request, template_name, context)
            user.spotname = spotname
            user.address = spotlocation
            user.user_type = 2
        user_number = number
        password = request.POST.get('password')
        if password is None:
            messages.warning(request, f'Enter your password')
            return render(request, template_name, context)
        user.email = request.POST.get('email')
        user.number = user_number
        user.password = password
        user.set_password(password)
        user.save()
        return redirect('login_user')

        # if the request is get method
    else:
        context = {}
        template_name = 'spotlocator/user_register.html'
        return render(request, template_name, context)


def login_view(request):
    # Post method
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == '1':
                return redirect('customer_dash')
            elif user.user_type == '2':
                return redirect('owners_profile')
            else:
                messages.info(request, f'Invalid Account, Please Register')
                return redirect('register')
        else:
            messages.warning(request, f'Invalid email or password supplied')
            return render(request, 'spotlocator/login_user.html')
     #for Get method
    else:
        return render(request, 'spotlocator/login_user.html')


def logout_view(request):
    logout(request)
    return redirect('login_user')


@login_required(redirect_field_name='owners_profile', login_url='login_user')
def owners_profiles(request):
    user = request.user
    if user.user_type != '2':
        messages.info(request, f'YOU ARE TRESPASSING YOUR BOUNDARY')
        return redirect('login_user')
    if request.method == 'POST':
        owner_form = OwnerProfileForm(request.POST, request.FILES, instance=request.user)
        if owner_form.is_valid():
            owner_form.save()
        messages.info(request, f'Your account has been updated!.')
        return redirect('owners_profile')

    else:
        owner_form = OwnerProfileForm(instance=request.user)
    context = {'form': owner_form}
    return render(request, 'spotlocator/owners_profiles.html', context)


@login_required(redirect_field_name='create_menu', login_url='login_user')
def create_menu(request):
    user = request.user
    if user.user_type != '2':
        messages.info(request, f'You are not permitted')
        return redirect('login_user')
    template_name = 'spotlocator/create_menu.html'
    if request.method == 'POST':
        menu_form = MenuCreateForm(request.POST)
        if menu_form.is_valid():
            menu_owner= menu_form.save(commit=False)
            menu_owner.owner = request.user
            menu_owner.save()
            return redirect('menu_list')
        else:
            messages.info(request, f'Invalid data supplied')
            return render(request, template_name, {'form': menu_form})
    else:
        menu_form = MenuCreateForm()
    context = {
        'form': menu_form
    }
    return render(request, template_name, context)

def menu_list(request):
    user = request.user
    if user.user_type != '2':
        messages.info(request, f'You are not permitted')
        return redirect('login_user')
    current_user = user
    template_name = 'spotlocator/menulist.html'
    menus = current_user.menulist_set.all() # associates the menulist items to the creator[current user]
    if menus:
        menus_total = menus.count()
        if menus_total > 0:
            messages.info(request, f'{menus_total} item is added, Add more!')
            return render(request, template_name, {'menus':menus})
    else:
        messages.info(request, f'You have zero menu item, Click the create-menu to Add!.')
        return render(request, template_name)
    return render(request, template_name)


@login_required(redirect_field_name='customer_dash', login_url='login_user')
def customer_dash(request):
    user = request.user
    if user.user_type != '1':
        messages.info(request, f'You are not permitted')
        return redirect('login_user')
    template_name = 'spotlocator/customer_dash.html'
    query = request.GET.get("q")
    search_list = User.objects.all()
    if query:
        search_list =search_list.filter(Q(state__icontains=query)|
                                         Q(city__icontains=query)|
                                          Q(address__icontains=query)).distinct()
        if search_list.exists():
            total_search = search_list.count()
            if total_search > 0:
                messages.success(request, f'We found {total_search} SharwamaSpots nearer to you!.')
                context={'search_list':search_list}
                return render(request, template_name, context)
        else:
            messages.success(request, f'Oops!!....None Found')
            return render(request, template_name)
    else:
        messages.info(request, f'Search for Sharwamspot nearer to you.')
    return render(request, template_name)










# def menu_details(request, menu_id):
#     # get the menu details of the searched query to the customer. for them to be able to connect
#     menu_details=get_object_or_404(MenuList, pk=menu_id)
#     template_name = 'spotlocator/menu_detail.html'
#     context = {'menu':menu_details}
#     return render(request, template_name, context)

