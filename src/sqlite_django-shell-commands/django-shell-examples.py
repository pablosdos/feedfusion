# ✗ pipenv run python manage.py shell

from product_feed_generator.models import Product
from product_feed_generator.models import FeedConfiguration, Feed

Serverkast_Product.objects.all().delete()
topsystemsfeed = Feed.objects.get(shop_name="TopSystems")
FeedConfiguration.objects.create(
    feed=feed_xyz, product_schema_for_final_field="", custom_calculation_units_list=""
)
feed_conf_from_current_shop_for_updating = FeedConfiguration.objects.filter(
    feed=feed_xyz
)


feed_conf_from_current_shop_for_updating = Feed.objects.filter(
    shop_name="TopSystems"
)
print(feed_conf_from_current_shop_for_updating)


#on the server
# cd /home/datafeeds/production/feedfusion/src
# % python3 -m pipenv run python manage.py shell
from product_feed_generator.models import Product, Feed
topsystemsfeed = Feed.objects.get(shop_name="TopSystems")
feed_conf_from_current_shop_for_updating = Product.objects.filter(
    feed=topsystemsfeed
)
print(feed_conf_from_current_shop_for_updating)
feed_conf_from_current_shop_for_updating.update(is_selected=True)