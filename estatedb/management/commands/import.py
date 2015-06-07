from django.core.management.base import BaseCommand, CommandError
from estatedb import models
import django.contrib.auth.models
import os
import yaml

class Command(BaseCommand):
    help = 'Import the catalogue data'

    def add_arguments(self, parser):
        parser.add_argument('catalogue', type=str)
        parser.add_argument('photo_dir', type=str)

    def handle(self, *args, **options):
        catalogue = args[0]
        photo_dir = args[1]

        cat_data = yaml.load(file(catalogue,'r'))
        
        article_types = dict([
            (type_name, models.ArticleType.objects.get_or_create( \
                name=type_name)[0])
            for type_name in cat_data['article_types']])
        for at in article_types.values():
            at.save()

        users = dict([
            (u.username, u) for u in
            django.contrib.auth.models.User.objects.all()])

        for loc_name, loc_data in cat_data['areas'].items():
            location = models.Location.objects.get_or_create( \
                        name=loc_name, code_prefix=loc_data['prefix'])[0]
            location.save()
            for item_data in loc_data['items']:
                article_data = {
                        'code':         item_data['ITEM'],
                        'name':         item_data['NAME'],
                        'location':     location,
                        'description':  item_data['DESCRIPTION'],
                        'article_type': article_types[\
                                item_data['ARTICLE TYPE']],
                }
                if item_data['AVAILABLE'] and \
                        (item_data['claimant'] is not None):
                    article_data['claimant'] = users[item_data['claimant']]
                item, new = models.Item.objects.get_or_create(
                        **article_data)
                item.save()
                if new:
                    for photo in item_data['photos']:
                        photo_name = os.path.basename(photo)
                        with open(os.path.join(photo_dir, photo),'r') as photo_file:
                            p = models.Photo(item=item)
                            p.save()
                            p.photo.save(photo_name, django.core.files.File(photo_file), True)
                            p.save()
