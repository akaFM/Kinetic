from django import template
from calendar import month_name

register = template.Library()

@register.filter
def monthIntToMonthString(monthInt):
    return month_name[monthInt]