from django import template
from datetime import datetime, date
import jdatetime

register = template.Library()

# -------------------------------------------------------------------------------------------------------------------------------------

def currency(value):
    return '{:,}'.format(int(value))
register.filter('currency', currency)


def get_jalali_date(value):
    date_format = "%Y-%m-%d"
    thisdate = datetime.strptime(str(value.date()), date_format)
    return jdatetime.date.fromgregorian(day = thisdate.day, month = thisdate.month, year = thisdate.year)
register.filter('to_jalali', get_jalali_date)


def get_jalalidate_with_month(value):
    date_format = "%Y-%m-%d"
    thisdate = datetime.strptime(str(value.date()), date_format)
    thisjalalidate = jdatetime.date.fromgregorian(day = thisdate.day, month = thisdate.month, year = thisdate.year)
    jalali_month = {
        1 : 'فروردین',
        2 : 'اردیبهشت',
        3 : 'خرداد',
        4 : 'تیر',
        5 : 'مرداد',
        6 : 'شهریور',
        7 : 'مهر',
        8 : 'آبان',
        9 : 'آذر',
        10 : 'دی',
        11 : 'بهمن',
        12 : 'اسفند'
    }
    return str(thisjalalidate.day) + ' ' + str(jalali_month[thisjalalidate.month]) + ' ' + str(thisjalalidate.year)
register.filter('to_jalali_month', get_jalalidate_with_month)