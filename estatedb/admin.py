from django.contrib import admin
import mptt.admin
import models
import django.core.urlresolvers
import django.utils.html

# Source: http://stackoverflow.com/questions/9919780/how-do-i-add-a-link-from-the-django-admin-page-of-one-object-to-the-admin-page-o
def add_link_field(
        target_model = None, field = '', app='', field_name='link',
        link_text=unicode):
    def add_link(cls):
        reverse_name = target_model or cls.model.__name__.lower()
        def link(self, instance):
            app_name = app or instance._meta.app_label
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            link_obj = getattr(instance, field, None) or instance
            url = django.core.urlresolvers.reverse(
                    reverse_path, args = (link_obj.id,))
            return django.utils.html.mark_safe(
                    "<a href='%s'>%s</a>" % (url, link_text(link_obj)))
        link.allow_tags = True
        link.short_description = reverse_name + ' link'
        setattr(cls, field_name, link)
        cls.readonly_fields = list(getattr(cls, 'readonly_fields', [])) + \
            [field_name]
        return cls
    return add_link

@add_link_field()
class ItemInlineAdmin(admin.TabularInline):
    model   = models.Item
    fk_name = 'location'
    fields  = [
            'code',
            'article_type',
            'name',
            'description',
            'claimant',
            'link',
    ]

class LocationAdmin(mptt.admin.MPTTModelAdmin):
    inlines = [
            ItemInlineAdmin
    ]
    list_display_links = [
            'full_name',
    ]
    list_display = [
            'full_name', 'item_count',
    ]
    search_fields = [
            'parent__name',
            'name',
    ]
    fields = [
            'name',
            'parent',
            'code_prefix',
            'next_code',
    ]
admin.site.register(models.Location, LocationAdmin)

class PhotoInlineAdmin(admin.StackedInline):
    model   = models.Photo

class ItemAdmin(admin.ModelAdmin):
    inlines = [
            PhotoInlineAdmin
    ]
    list_display_links = [
            'name',
    ]
    list_display = [
            'location',
            'code',
            'name',
    ]
    search_fields = [
            'location__full_name',
            'name',
            'code',
    ]
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.ArticleType, admin.ModelAdmin)
