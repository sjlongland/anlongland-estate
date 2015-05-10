from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404
import models

# Create your views here.

def index(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    context = {
            'title': 'Estate index',
            'authenticated_user': request.user,
            'locations': models.Location.objects.filter(
                parent__isnull=True)
    }
    return render(request, 'estatedb/index.html', context)

def all(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    context = {
            'title': 'Estate index',
            'authenticated_user': request.user,
            'locations': models.Location.objects.all(),
    }
    return render(request, 'estatedb/all.html', context)

def location(request, location_id):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    try:
        location = models.Location.objects.get(pk=location_id)
    except models.Location.DoesNotExist:
        raise Http404("Location does not exist")

    if location.parent_item.count():
        parent_item = location.parent_item.all()[0]
    else:
        parent_item = None

    return render(request, 'estatedb/location.html', {
        'location': location,
        'title': 'Location: %s' % location.name,
        'authenticated_user': request.user,
        'parent': location.parent,
        'parent_item': parent_item,
        'child_locations': location.children.all(),
        'child_items': location.child_items.all(),
    })

def photo(request, photo_id):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

def item(request, item_id):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    try:
        item = models.Item.objects.get(pk=item_id)
    except models.Item.DoesNotExist:
        raise Http404("Item does not exist")

    return render(request, 'estatedb/item.html', {
        'title': 'Item: %s' % item.name,
        'authenticated_user': request.user,
        'item': item,
        'photos': item.photo_set.all(),
        })
