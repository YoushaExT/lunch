from django import template
import hashlib
import datetime

register = template.Library()


def sq(value):
    return value ** 2


def khana_password(value):
    value = str(value)
    value = value.encode('utf-8')
    hashed_pin = hashlib.sha224(value)
    return hashed_pin.hexdigest()


def date_to_day(value):
    return value.strftime("%A")


def filter_by_user(value, user_id):
    return value.filter(user_id=int(user_id))


def filter_by_shop(value, shop_id):
    return value.filter(item_id__shop_id=int(shop_id))


# for debugging in templates
def type_filter(value):
    return type(value)


# for debugging in templates
def vars_filter(value):
    return vars(value)


def is_hidden_input_filter(value):
    from django.forms.widgets import HiddenInput
    return isinstance(value.field.widget, HiddenInput)


def multiply(value, number):
    return value*number

@register.simple_tag
def setvar(value=None):
    return value


register.filter(multiply)
register.filter(is_hidden_input_filter)
register.filter(vars_filter)
register.filter('type', type_filter)
register.filter('filter_by_shop', filter_by_shop)
register.filter('filter_by_user', filter_by_user)
register.filter('sq', sq)
register.filter('khana_password', khana_password)
register.filter('date_to_day', date_to_day)


# orders|order_filter:"7"