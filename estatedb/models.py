from django.db import models
import mptt.models
import django.contrib.auth.models

class Location(mptt.models.MPTTModel):
    parent = mptt.models.TreeForeignKey(
            'self', null=True, blank=True, related_name='children')
    code_prefix     = models.CharField(max_length=3, unique=True)
    next_code       = models.PositiveIntegerField(default=0)
    name            = models.CharField(max_length=64)
    full_name       = models.CharField(max_length=256)

    path            = property(lambda s : \
            ((s.parent and s.parent.path) or []) + [s.name])
    parent_name     = property(lambda s : (s.parent and \
            s.parent.full_name) or None)
    item_count      = property(lambda s : s.item_set.count() + sum([\
            c.item_count for c in s.children.all()] + [0]))

    def __unicode__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.full_name = u'/'.join(self.path)
        return super(Location, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('parent','name')
        ordering        = ['name']

    def _get_new_code(self, next_code=None):
        return u'%s_%08d' % (self.code_prefix, next_code or self.next_code)

    def get_new_code(self):
        code = self._get_new_code()
        next_code = self.next_code + 1
        while self.child_items.filter(\
                code__exact=self._get_new_code(next_code)).count() > 0:
            next_code += 1
        self.next_code = next_code
        self.save()
        return code

class ArticleType(models.Model):
    name                = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering        = ['name']

class Item(models.Model):
    code                = models.CharField(max_length=12,
                            unique=True, null=True, blank=True)
    location            = models.ForeignKey(Location,
                            related_name='child_items')
    article_type        = models.ForeignKey(ArticleType)
    name                = models.CharField(max_length=64)
    description         = models.CharField(max_length=256)
    claimant            = models.ForeignKey(
            django.contrib.auth.models.User, null=True, blank=True)
    contents            = models.ForeignKey(Location, null=True,
            blank=True, related_name='parent_item')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not bool(self.code):
            self.code = self.location.get_new_code()
        super(Item, self).save(*args, **kwargs)

class Photo(models.Model):
    item                = models.ForeignKey(Item)
    photo               = models.ImageField()
