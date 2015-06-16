from django import template
import datetime
from datetime import date
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse


register = template.Library()


@register.filter(name='get_active_label')
def active_label(active):
    span = ''
    if active:
        span = '<span class="label label-success">active</span>'
    else:
        span = '<span class="label label-danger">inactive</span>'
    return mark_safe(span)


@register.filter(name='get_status_label')
def status_label(status):
    span = ''
    if status == 0:
        span = '<span class="label label-primary">ready to begin</span>'
    elif status == 1:
        span = '<span class="label label-info">in progress</span>'
    elif status == 2:
        span = '<span class="label label-completed">completed</span>'
    elif status == 3:
        span = '<span class="label label-warning">on hold</span>'
    return mark_safe(span)


@register.filter(name='get_daysleft_label')
def get_daysleft_label(days, active):
    span = ''
    if active:
        if days < 0:
            span = '<span class="label label-danger">'
            span = span + '<span class="glyphicon glyphicon-exlamation-sign">'
            span = span + '</span>' + str(days*-1) + ' days overdue</span>'
        elif days == 0:
            span = '<span class="label label-danger">'
            span = span + '<span class="glyphicon glyphicon-exclamation-sign">'
            span = span + '</span> due today</span>'
        elif days > 0 and days < 15:
            span = '<span class="label label-warning">'
            span = span + str(days) + ' days left</span>'
        else:
            span = '<span class="label label-info">'
            span = span + str(days) + ' days left</span>'
        return mark_safe(span)


@register.filter(name='get_dayssince_label')
def get_dayssince_label(days, active):
    span = ''
    if active:
        if days > 0:
            span = '<span class="label label-info">'
            span = span + str(days) + ' days since</span>'
        return mark_safe(span)

@register.filter(name='get_duration')
def get_duration(duration):
    span = "<hr class='gantt-{{ c.ptask_type }}' width="+str(duration)+"px>"
    return mark_safe(span)


@register.filter(name='get_breadcrumbs')
def get_breadcrumbs(node):
    bc = '<span>'
    for a in node.get_ancestors():
        link = reverse('ptasks:ptask_detail', args=[str(a.pk)])
        bc = bc + '<a href="' + link + '">' + a.name + '</a>='
    if not node.is_root_node():
        bc = bc + '<strong>'+ node.name + '</strong>'
    bc = bc + '\n</span><br><br>'
    return mark_safe(bc)

@register.filter(name='get_formated_start_date')
def get_formated_start_date(ptask):
    from_date = date(1970,1,1);
    return ((ptask.start_date - from_date).days+1)*24*3600*1000

@register.filter(name='get_formated_end_date')
def get_formated_end_date(ptask):
    from_date = date(1970,1,1);
    return ((ptask.due_date - from_date).days+1)*24*3600*1000
