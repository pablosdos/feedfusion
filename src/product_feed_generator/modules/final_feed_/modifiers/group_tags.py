from django.db.models.query import QuerySet

from product_feed_generator.models import Product, GroupTag


def apply_grouptag_condition_adjustments(
    selected_products_qs: QuerySet[Product],
    selected_products_copy: list[dict],
) -> list[dict]:
    product: Product
    for index, product in enumerate(selected_products_qs):
        tag: GroupTag
        #summarize all price changes (because of tags) of 1 product and apply them
        sum_percentage_factor: float = 100.0
        for tag in product.group_tags.all():
            sum_percentage_factor += tag.price_percentage_factor
        selected_products_copy[index]["sales_price_excluding_tax"] = "%.2f" % (
            product.sales_price_excluding_tax / 100 * sum_percentage_factor
        )

    return selected_products_copy
