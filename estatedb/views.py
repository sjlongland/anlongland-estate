from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404, HttpResponseForbidden
import django.contrib.auth.views
import models

# Create your views here.

def index(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    context = {
            'title': 'Estate index',
            'authenticated_user': request.user,
            'locations': models.Location.objects.filter(
                parent__isnull=True).order_by('full_name'),
    }
    return render(request, 'estatedb/index.html', context)

def all(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    context = {
            'title': 'Estate index',
            'authenticated_user': request.user,
            'locations': \
                    models.Location.objects.all().order_by('full_name'),
    }
    return render(request, 'estatedb/all.html', context)

def location(request, location_id):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    try:
        location = models.Location.objects.get(pk=location_id)
    except models.Location.DoesNotExist:
        raise Http404("Location does not exist")

    siblings = list(models.Location.objects.filter(
            parent=location.parent).order_by('full_name'))
    sibling_ids = [l.id for l in siblings]
    my_order = sibling_ids.index(location.id)

    if my_order > 0:
        prev_loc = siblings[my_order-1]
    else:
        prev_loc = None

    if my_order < len(sibling_ids)-1:
        next_loc = siblings[my_order+1]
    else:
        next_loc = None

    if location.parent_item.count():
        parent_item = location.parent_item.all()[0]
    else:
        parent_item = None

    return render(request, 'estatedb/location.html', {
        'location': location,
        'prev_loc': prev_loc,
        'next_loc': next_loc,
        'title': 'Location: %s' % location.name,
        'authenticated_user': request.user,
        'parent': location.parent,
        'parent_item': parent_item,
        'child_locations': location.children.all(),
        'child_items': location.child_items.all().order_by('code'),
    })

def photo(request, photo_id):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

def mine(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    claimed = models.Item.objects.filter(
            claimant=request.user).order_by('code')

    return render(request, 'estatedb/mine.html', {
        'title': u'My items',
        'authenticated_user': request.user,
        'claimed': claimed,
    })

def claimed(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if not request.user.is_superuser:
        return HttpResponseForbidden('This requires superuser access')

    claimed = models.Item.objects.exclude(
            claimant__isnull=True).order_by('code')

    return render(request, 'estatedb/claimed.html', {
        'title': u'Claimed items',
        'authenticated_user': request.user,
        'claimed': claimed,
    })

def item(request, item_id):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    try:
        item = models.Item.objects.get(pk=item_id)
    except models.Item.DoesNotExist:
        raise Http404("Item does not exist")

    unclaimed = item.claimant is None
    if not unclaimed:
        mine = item.claimant.username == request.user.username
    else:
        mine = False

    if request.method == 'POST':
        if unclaimed and (request.POST['action'] == 'claim'):
            item.claimant = request.user
            item.save()
            mine = True
            unclaimed = False
        elif mine and (request.POST['action'] == 'unclaim'):
            item.claimant = None
            item.save()
            mine = False
            unclaimed = True

    siblings = list(models.Item.objects.filter(
            location=item.location).order_by('code'))
    sibling_ids = [i.id for i in siblings]
    my_order = sibling_ids.index(item.id)

    if my_order > 0:
        prev_item = siblings[my_order-1]
    else:
        prev_item = None

    if my_order < len(sibling_ids)-1:
        next_item = siblings[my_order+1]
    else:
        next_item = None

    return render(request, 'estatedb/item.html', {
        'title': u'Item %s: %s' % (item.code, item.name),
        'prev_item': prev_item,
        'next_item': next_item,
        'authenticated_user': request.user,
        'item': item,
        'unclaimed': unclaimed,
        'mine': mine,
        'photos': item.photo_set.all(),
        })

def logout(request):
    return django.contrib.auth.views.logout(request,
            next_page='/',
            template_name='estatedb/logged_out.html')
def password_change(request):
    return django.contrib.auth.views.password_change(request,
            post_change_redirect='/changedpw.html',
            template_name='estatedb/password_change_form.html')
def password_change_done(request):
    return django.contrib.auth.views.password_change_done(request,
            template_name='estatedb/password_change_done.html')
