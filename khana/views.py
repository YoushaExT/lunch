from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import FoodItem, Order, Shop, Date, TempUser
from django import forms
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# import hashlib
from django.db.models import Sum


class AddFoodForm(forms.Form):

    def __init__(self, *args, shop_id=None, updated_id=None, **kwargs):
        self.shop_id = shop_id
        self.updated_id = updated_id
        super(AddFoodForm, self).__init__(*args, **kwargs)
        if not self.shop_id:
            all_foods = FoodItem.objects.all()
        else:
            all_foods = FoodItem.objects.filter(shop=self.shop_id)
        CHOICES = [(food.id, f'{food.shop} - {food.name} - {food.price}') for food in all_foods.order_by('shop', 'price')]
        CHOICES = tuple(CHOICES)
        self.fields['food'] = forms.ChoiceField(choices=CHOICES)
        self.fields['updated_id'] = forms.IntegerField(initial=self.updated_id, required=False)
        self.fields['updated_id'].widget = forms.HiddenInput()

    # QUANTITY_CHOICES = tuple([(x, x) for x in range(1, 11)])
    # quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, empty_value=1, coerce=int)
    quantity = forms.IntegerField(initial=1)
    quantity.widget.attrs.update({'min': 1, 'max': 10})
    # quantity = forms.ChoiceField(choices=QUANTITY_CHOICES)


class SelectShopForm(forms.Form):

    def __init__(self, *args, updated_id=None, default_shop=None, **kwargs):
        self.updated_id = updated_id
        super(SelectShopForm, self).__init__(*args, **kwargs)
        self.fields['updated_id'] = forms.IntegerField(initial=self.updated_id, required=False)
        self.fields['updated_id'].widget = forms.HiddenInput()

        if default_shop:  # after changing dropdown
            selected_shop = Shop.objects.get(pk=default_shop)
            CHOICES = [(selected_shop.id, selected_shop.name)]  # first the selected shop
            all_shops = Shop.objects.exclude(pk=default_shop)
            CHOICES += [(shop.id, shop.name) for shop in all_shops]  # then remaining shops
            CHOICES += [(0, 'All Shops')]
        else:  # first time
            CHOICES = [(0, 'All Shops')]
            all_shops = Shop.objects.all()
            CHOICES += [(shop.id, shop.name) for shop in all_shops]

        CHOICES = tuple(CHOICES)
        self.fields['shop'] = forms.ChoiceField(choices=CHOICES)
        self.fields['shop'].widget.attrs.update({'id': 'shop_selector', 'onchange': 'myShopFunction()'})


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    # last_name.widget.attrs.update({'id': 'special'})
    username = forms.CharField(max_length=64)
    email = forms.EmailField(max_length=128)

    password = forms.CharField(label='4 Digit PIN')
    password.widget = forms.PasswordInput()
    password.widget.attrs.update({
        'id': 'p1',
        'class': 'form-control',
        'placeholder': 'PIN',
        'maxlength': 4,
    })

    first_name.widget.attrs.update({'class': 'form-control'})
    last_name.widget.attrs.update({'class': 'form-control'})
    username.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control'})
    # pin = forms.IntegerField(min_value=1000, max_value=9999, label='4 Digit PIN')


class SelectUserForm(forms.Form):
    all_users = User.objects.all()
    # full_name = person.first + person.last
    CHOICES_USER = [(user.id, f'{user.first_name} {user.last_name}') for user in all_users]
    CHOICES_USER = tuple(CHOICES_USER)
    user = forms.ChoiceField(choices=CHOICES_USER)


class SelectDateForm(forms.Form):

    def __init__(self, *args, default_date=None, **kwargs):
        # self.default_date = default_date
        super(SelectDateForm, self).__init__(*args, **kwargs)
        if default_date:
            print(default_date)
            all_dates = Date.objects.exclude(date=default_date).order_by('-date')
            # print(all_dates)
            initial_date = Date.objects.get(date=default_date)
            # print(initial_date)
            CHOICES_DATE = [(initial_date.id, f'{initial_date.date}')]
            OTHER_DATE = [(date.id, f'{date.date}') for date in all_dates]
            CHOICES_DATE += OTHER_DATE
            CHOICES_DATE += [(0, 'All Dates')]
            CHOICES_DATE = tuple(CHOICES_DATE)
            # print(CHOICES_DATE)
        else:
            all_dates = Date.objects.all().order_by('-date')
            CHOICES_DATE = [(0, 'All Dates')]
            OTHER_DATE = [(date.id, f'{date.date}') for date in all_dates]
            CHOICES_DATE += OTHER_DATE
            CHOICES_DATE = tuple(CHOICES_DATE)


        # OTHER_DATE = [(date.id, f'{date.date}') for date in all_dates]
        # CHOICES_DATE += OTHER_DATE
        # CHOICES_DATE = tuple(CHOICES_DATE)

        self.fields['id'] = forms.ChoiceField(choices=CHOICES_DATE, label='Date')
        self.fields['id'].widget.attrs.update({'id': 'date_selector', 'onchange': 'myDateFunction()'})


class FilterShopAndPersonForm(forms.Form):

    def __init__(self, *args, default_shop=None, default_people=None, shops=Shop.objects.all(), peoples=User.objects.all(), people_disabled=False, **kwargs):

        super(FilterShopAndPersonForm, self).__init__(*args, **kwargs)

        if default_shop:  # after changing dropdown
            selected_shop = shops.get(pk=default_shop)
            CHOICES = [(selected_shop.id, selected_shop.name)]  # first the selected shop
            all_shops = shops.exclude(pk=default_shop)
            CHOICES += [(shop.id, shop.name) for shop in all_shops]  # then remaining shops
            CHOICES += [(0, 'All Shops')]
        else:  # first time
            CHOICES = [(0, 'All Shops')]
            all_shops = shops
            CHOICES += [(shop.id, shop.name) for shop in all_shops]

        CHOICES = tuple(CHOICES)
        self.fields['shop'] = forms.ChoiceField(choices=CHOICES)
        self.fields['shop'].widget.attrs.update({'id': 'shop_selector', 'onchange': 'myFilterFunction()'})

        # print(default_people)
        # print(peoples)
        # people
        if default_people:  # after changing dropdown
            selected_people = peoples.get(pk=default_people)
            # print(selected_people, selected_people.id, f'{selected_people.first_name} {selected_people.last_name}')
            CHOICES = [(selected_people.id, f'{selected_people.first_name} {selected_people.last_name}')]  # first the selected shop
            all_people = peoples.exclude(pk=default_people)
            CHOICES += [(p.id, f'{p.first_name} {p.last_name}') for p in all_people]
            CHOICES += [(0, 'Everyone')]
        else:  # first time
            CHOICES = [(0, 'Everyone')]
            all_people = peoples
            CHOICES += [(p.id, f'{p.first_name} {p.last_name}') for p in all_people]

        CHOICES = tuple(CHOICES)
        self.fields['people'] = forms.ChoiceField(choices=CHOICES)
        self.fields['people'].widget.attrs.update({'id': 'people_selector', 'onchange': 'myFilterFunction()'})
        # todo privacy non admin doesnt see people dropdown
        if people_disabled:
            print('hiding')
            # self.fields['people'].widget = forms.HiddenInput()
            self.fields['people'].widget.attrs.update({'hidden': 'True'})
            self.fields['people'].label = ''  # hide label as well

        # todo hidden field for date
        self.fields['date'] = forms.CharField()
        self.fields['date'].widget = forms.HiddenInput()
        self.fields['date'].widget.attrs.update({'id': 'hidden_date'})


# Create your views here.
def index(request, date_id=None):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))


    # if a date is provided
    if date_id:
        # is_today = False
        # date_object = None
        today = datetime.datetime.now().date()
        if Date.objects.filter(date=today).exists():
            date_object = Date.objects.get(date=today)
        else:
            date_object = Date(date=today)
            date_object.save()

        today_id = date_object.id
        if Date.objects.filter(pk=date_id).exists():
            date_object = Date.objects.get(pk=date_id)
            is_today = today == date_object.date
        else:
            # if invalid date id e.g. 999999 is provided, redirect to today's view
            return HttpResponseRedirect(reverse('table', args=[date_object.id]))

        date_form = SelectDateForm(default_date=date_object.date)
        all_orders = False
        dates_orders = Order.objects.filter(date_id=date_object)
        date = date_object.date
    # today if no date is provided - todo changing this
    # todo - all orders
    else:
        is_today = False
        today = datetime.datetime.now().date()

        if Date.objects.filter(date=today).exists():
            date_object = Date.objects.get(date=today)
        else:
            date_object = Date(date=today)
            date_object.save()
        today_id = date_object.id
        date_form = SelectDateForm()
        all_orders = True
        dates_orders = Order.objects.all()
        date = None

    # dates_orders = Order.objects.filter(date_id=date_object)
    # dates_orders = Order.objects.all()
    # todo privacy, non staff should only be able to view their own
    people_disabled = False
    if not request.user.is_staff:
        dates_orders = dates_orders.filter(user_id=request.user)
        people_disabled = True

    dates_items = dates_orders.values_list('item_id_id', flat=True).distinct()
    dates_shops = FoodItem.objects.all().filter(id__in=dates_items).values_list('shop_id', flat=True).distinct()
    shops = Shop.objects.filter(pk__in=dates_shops)
    # ppl who ordered on this date
    dates_people = dates_orders.values_list('user_id_id', flat=True).distinct()
    peoples = User.objects.filter(pk__in=dates_people)

    sum_price = sum(o.item_id.price*o.quantity for o in dates_orders)

    # return HttpResponse(date_object.date)
    return render(request, 'khana/index.html', {
        'today_id': today_id,
        'date': date,
        'orders': dates_orders.order_by('-pk'),
        'sum': sum_price,
        'date_form': date_form,
        # 'date_form': SelectDateForm(default_date=date_object.date),
        # 'date_form': SelectDateForm(),
        'is_today': is_today,
        'all_orders': all_orders,
        # todo privacy people_disabled
        'filter_form': FilterShopAndPersonForm(shops=shops, peoples=peoples, people_disabled=people_disabled),
        # 'shops': shops,
        # 'people': people,
    })


def add(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':

        # submitted order instead of shop filter
        form = AddFoodForm(request.POST)
        if form.is_valid():
            food = form.cleaned_data['food']
            quantity = form.cleaned_data['quantity']
            # order_id = form.cleaned_data['updated_id']
            if 'updated_id' in form.cleaned_data:
                order_id = form.cleaned_data['updated_id']
                if order_id:
                    Order.objects.get(pk=order_id).delete()

        user = request.user.id
        today = datetime.datetime.now().date()
        if Date.objects.filter(date=today).exists():
            today_object = Date.objects.get(date=today)
        else:
            today_object = Date(date=today)
            today_object.save()

        this_user = User.objects.get(pk=user)
        this_food = FoodItem.objects.get(pk=food)
        new_order = Order(quantity=quantity, date_id=today_object, user_id=this_user, item_id=this_food)
        new_order.save()

        return HttpResponseRedirect(reverse('todays_orders'))

    else:
        return render(request, 'khana/add.html', {
            # 'foods': FoodItem.objects.all(),
            'shops': Shop.objects.all(),
            'form': AddFoodForm(),
            # 'user_form': SelectUserForm(),
            'shop_form': SelectShopForm(),
        })


def shop_filter(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        form = SelectShopForm(request.POST)
        if form.is_valid():
            shop = form.cleaned_data['shop']
            order_id = form.cleaned_data['updated_id']

            if shop != '0':
                # show filtered food items
                food_form = AddFoodForm(shop_id=shop, updated_id=order_id)
                shop_form = SelectShopForm(updated_id=order_id, default_shop=shop)
            else:
                # show all food items
                food_form = AddFoodForm(updated_id=order_id)
                shop_form = SelectShopForm(updated_id=order_id)

            return render(request, 'khana/add.html', {
                'shops': Shop.objects.all(),
                'form': food_form,
                'shop_form': shop_form,
            })

    else:
        return HttpResponseRedirect(reverse('add'))


def login_view(request):
    if request.method == 'POST':
        if not request.POST['username'] or not request.POST['password']:
            return render(request, 'khana/login.html', {
                'message': 'Please fill in both fields'
            })
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:

            if TempUser.objects.filter(username=username).exists():
                temp_user = TempUser.objects.get(username=username)

                message = f'{temp_user.first_name} {temp_user.last_name}, Please wait for approval by the admin'

            else:
                message = 'Invalid credentials'


            return render(request, 'khana/login.html', {
                'message': message,
            })
    return render(request, 'khana/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'khana/login.html', {
        'message': 'Logged out',
    })


def register(request):
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():

            first_name = registration_form.cleaned_data['first_name']
            last_name = registration_form.cleaned_data['last_name']

            username = registration_form.cleaned_data['username'].lower()
            email = registration_form.cleaned_data['email'].lower()
            # hashed_pin = registration_form.cleaned_data['hidden_pin']
            hashed_pin = registration_form.cleaned_data['password']

            # todo email/username already taken
            display_error = False
            message = ''

            # todo capitalize

            first_name = first_name.split()
            last_name = last_name.split()
            for z in (first_name, last_name):
                for i, x in enumerate(z):
                    if not x.isalpha():
                        display_error = True
                        message = 'Only alphabets allowed in names'
                        break
                    z[i] = z[i].capitalize()

            first_name = ' '.join(first_name)
            last_name = ' '.join(last_name)

            users = User.objects.all()
            temp_users = TempUser.objects.all()
            emails = users.values_list('email', flat=True)
            temp_emails = set(temp_users.values_list('email', flat=True))
            emails = set(emails).union(temp_emails)

            usernames = users.values_list('username', flat=True)
            temp_usernames = set(temp_users.values_list('username', flat=True))
            usernames = set(usernames).union(temp_usernames)

            if email in emails:
                message += f'{email} is already in use! Please use a different email\n'
                display_error = True
            if username in usernames:
                message += f'{username} is already in use! Please use a different username\n'
                display_error = True

            if ' ' in username:
                message += 'Spaces not allowed in username\n'
                display_error = True

            if display_error:
                return render(request, 'khana/register.html', {
                    'registration_form': RegistrationForm(label_suffix=''),
                    'message': message
                })

            # todo only techwards email:
            # import re
            # techwards_email = re.findall('@techwards.co$', email)
            # if not techwards_email:
            #     return render(request, 'khana/register.html', {
            #         'registration_form': RegistrationForm(label_suffix=''),
            #         'message': 'Please use your techwards email'
            #     })

            # pin = str(registration_form.cleaned_data['pin'])  # convert int pin to str
            # hashed_pin = pin.encode('utf-8')
            # hashed_pin = hashlib.sha224(hashed_pin)
            # hashed_pin = hashed_pin.hexdigest()  # use this instead

            temp_user = TempUser(username=username, password=hashed_pin, email=email,
                                 first_name=first_name, last_name=last_name)
            temp_user.save()
            return render(request, 'khana/login.html', {
                'message': 'Registered Successfully, Waiting for Approval'
            })
        else:
            return render(request, 'khana/register.html', {
                'registration_form': RegistrationForm(label_suffix=''),
                'message': 'Some error'
            })
    return render(request, 'khana/register.html', {
        'registration_form': RegistrationForm(label_suffix='')
    })


def approve_user(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':

        approved_user_id = request.POST['approved_user']
        approved_user = TempUser.objects.get(pk=approved_user_id)
        username = approved_user.username
        pin = str(approved_user.password)
        email = approved_user.email
        first_name = approved_user.first_name
        last_name = approved_user.last_name
        user = User.objects.create_user(username=username, password=pin, email=email,
                                        first_name=first_name, last_name=last_name)
        approved_user.delete()

        return HttpResponseRedirect(reverse('approve'))

    pending_users = TempUser.objects.all()
    return render(request, 'khana/approve.html', {
        'pending_users': pending_users
    })


def delete_order(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        order_id = request.POST['order_id']
        Order.objects.get(pk=order_id).delete()
    return HttpResponseRedirect(reverse('index'))


def delete_temp(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        user_id = request.POST['user_id']
        TempUser.objects.get(pk=user_id).delete()
    return HttpResponseRedirect(reverse('approve'))


def update_order(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        order_id = request.POST['order_id']
        return render(request, 'khana/add.html', {
            'foods': FoodItem.objects.all(),
            'shops': Shop.objects.all(),
            'form': AddFoodForm(updated_id=order_id),
            # 'user_form': SelectUserForm(),
            'shop_form': SelectShopForm(updated_id=order_id),
        })


def all_my_orders(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    my_orders = Order.objects.filter(user_id=request.user.id)
    sum_price = sum(o.item_id.price * o.quantity for o in my_orders)

    return render(request, 'khana/all.html', {
        'orders': my_orders.order_by('-pk'),
        'sum': sum_price,
    })


# index page but filtered
def filtered_index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        form = FilterShopAndPersonForm(request.POST)
        if form.is_valid():
            shop = form.cleaned_data['shop']
            people = form.cleaned_data['people']

            date = form.cleaned_data['date']

            if date and date != 'None':

                # return HttpResponse(date)
                # is_today = False
                d = datetime.datetime.strptime(date, "%B %d, %Y").date()
                date_object = Date.objects.get(date=d)

                today = datetime.datetime.now().date()
                if Date.objects.filter(date=today).exists():
                    d_o = Date.objects.get(date=today)
                else:
                    d_o = Date(date=today)
                    d_o.save()

                today_id = d_o.id
                is_today = date_object == d_o
                date_form = SelectDateForm(default_date=date_object.date)
                all_orders = False
                dates_orders = Order.objects.filter(date_id=date_object)
                date = date_object.date

            # today if no date is provided - todo change this
            else:
                # return HttpResponse(date)
                is_today = True
                today = datetime.datetime.now().date()

                if Date.objects.filter(date=today).exists():
                    date_object = Date.objects.get(date=today)
                else:
                    date_object = Date(date=today)
                    date_object.save()
                today_id = date_object.id
                date_form = SelectDateForm()
                all_orders = True
                dates_orders = Order.objects.all()
                date = None

            # todo privacy, non staff should only be able to view their own
            people_disabled = False
            if not request.user.is_staff:
                dates_orders = dates_orders.filter(user_id=request.user)
                people_disabled = True
            # dates_orders = Order.objects.filter(date_id=date_object)

            # sum_price = sum(o.item_id.price * o.quantity for o in dates_orders)

            # food items on this date
            # print(dates_orders)
            dates_items = dates_orders.values_list('item_id_id', flat=True).distinct()
            dates_shops = FoodItem.objects.all().filter(id__in=dates_items).values_list('shop_id', flat=True).distinct()
            shops = Shop.objects.filter(pk__in=dates_shops)
            # print(shops)
            # ppl who ordered on this date
            dates_people = dates_orders.values_list('user_id_id', flat=True).distinct()
            peoples = User.objects.filter(pk__in=dates_people)
            # return HttpResponse(peoples)

            shop2 = shop
            people2 = people

            if shop == '0' and people == '0':
                shop2 = None
                people2 = None
            elif shop == '0':
                shop2 = None
                dates_orders = dates_orders.filter(user_id=people)
            elif people == '0':
                people2 = None
                dates_orders = dates_orders.filter(item_id__shop_id=shop)
            else:
                dates_orders = dates_orders.filter(item_id__shop_id=shop).filter(user_id=people)

            # print(dates_orders)
            # todo privacy people_disabled
            filter_form = FilterShopAndPersonForm(default_shop=shop2, default_people=people2, shops=shops,
                                                  peoples=peoples, people_disabled=people_disabled)

            sum_price = sum(o.item_id.price * o.quantity for o in dates_orders)
            return render(request, 'khana/index.html', {
                'today_id': today_id,
                'date': date,
                'orders': dates_orders.order_by('-pk'),
                'sum': sum_price,
                'all_orders': all_orders,
                'date_form': date_form,
                # 'date_form': SelectDateForm(default_date=date_object.date),
                'is_today': is_today,
                # 'shop': shop,
                # 'people': people,
                'filter_form': filter_form,
            })
        else:
            return HttpResponse(request.POST.items())

    else:
        return HttpResponseRedirect(reverse('index'))


def todays_orders(request):
    today = datetime.datetime.now().date()
    if Date.objects.filter(date=today).exists():
        date_object = Date.objects.get(date=today)
    else:
        date_object = Date(date=today)
        date_object.save()
    return HttpResponseRedirect(reverse('table', args=[date_object.id]))


def print_orders(request):
    today = datetime.datetime.now().date()
    if Date.objects.filter(date=today).exists():
        date_object = Date.objects.get(date=today)
    else:
        date_object = Date(date=today)
        date_object.save()

    dates_orders = Order.objects.filter(date_id=date_object)

    # all foods today
    dates_items = dates_orders.values_list('item_id_id', flat=True).distinct()
    # all shops today
    dates_shops = FoodItem.objects.all().filter(id__in=dates_items).values_list('shop_id', flat=True).distinct()
    orders_by_shop = []
    shops = Shop.objects.all()
    foods = FoodItem.objects.all()
    users = User.objects.all()

    orders_by_person = []
    dates_persons = dates_orders.values_list('user_id_id', flat=True).distinct()
    for person_id in dates_persons:

        # orders of this person
        orders = dates_orders.filter(user_id_id=person_id)
        total = 0
        for order in orders:
            total += order.quantity * order.item_id.price
        person = users.get(pk=person_id)
        dict_person_order = {
            'person': person,
            'orders': orders,
            'total': total,
        }
        orders_by_person.append(dict_person_order)

    for shop_id in dates_shops:

        orders = dates_orders.filter(item_id__shop_id=shop_id)
        item_ids = orders.values_list('item_id_id', flat=True).distinct()

        list_orders = []
        for item_id in item_ids:
            dict_order = {}
            item = foods.get(pk=item_id)
            # print(item)
            order = orders.filter(item_id=item_id)
            # print(order)
            # name, sum quantity, sum price
            q = order.aggregate(Sum('quantity'))
            quantity = q['quantity__sum']

            # total = order.aggregate(Sum('item_id__price'))
            total = quantity*item.price
            # print(quantity, total)
            dict_order['item'] = item
            dict_order['quantity'] = quantity
            dict_order['total'] = total
            list_orders.append(dict_order)
        # print(list_orders)
        shop = {'object': shops.get(pk=shop_id), 'order': list_orders}
        orders_by_shop.append(shop)

    return render(request, 'khana/print.html', {
        # 'today_id': today_id,
        # 'date': date,
        'orders_by_shop': orders_by_shop,
        'orders': dates_orders,
        'orders_per_person': orders_by_person,
        # 'sum': sum_price,
        # 'date_form': date_form,
        # 'is_today': is_today,
        # 'all_orders': all_orders,
        # 'filter_form': FilterShopAndPersonForm(shops=shops, peoples=peoples),
    })


def default(request, useless=None):
    return HttpResponseRedirect(reverse('index'))


def send_a_mail(request):
    from django.core.mail import send_mail
    print('Sending email!')
    send_mail(
        'Subject here 2',
        'Here is the message 2.!!',
        'yousha.arshad@techwards.co',
        ['yousha234@gmail.com'],
        fail_silently=False,
    )

    return HttpResponseRedirect(reverse('index'))