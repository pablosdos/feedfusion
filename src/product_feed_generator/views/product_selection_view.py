from django.template.loader import get_template
from django.http import HttpResponse
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from product_feed_generator.models import Product, Feed, GroupTag
from product_feed_generator.forms import (
    ProductSelectForFinalFeedForm,
    SortingSelectForm,
    NewGroupTagForm,
)
from product_feed_generator.modules.final_feed_.base import FinalFeed_
from product_feed_generator.modules.final_feed_.output.xml import (
    create_final_feed_xml_file,
)


@login_required
def product_selection_view(request):
    toast_message: str = None
    group_tags: GroupTag = GroupTag.objects.all()
    template = get_template("product_selection_page.html")
    # if request.method == "GET":
    selected_products_from_database: QuerySet[Product] = Product.objects.filter(
        is_selected=True
    )
    paginator = Paginator(selected_products_from_database, 50)
    page_number = request.GET.get("page")
    paginator_control_with_products_queryset = paginator.get_page(page_number)
    paginated_form = ProductSelectForFinalFeedForm(
        paginator_control_with_products_queryset
    )
    feeds = Feed.objects.all()
    if "add-to-product-collection-form" in request.POST:
        finalfeed = FinalFeed_()
        # # topsystems_finalfeed._apply_configuration_scheme(complete_topsystems_products_list)
        # context = finalfeed.save_xml_file(request)
        finalfeed.save_xml_file(request)
    if not "sort_type" in locals():
        sort_type: str = "Sort by"
    if not "sorting_option_form" in locals():
        sorting_option_form = SortingSelectForm()
    new_group_tag_form = NewGroupTagForm()
    if "add-group-tag-form" in request.POST:
        new_group_tag_form = NewGroupTagForm(request.POST)
        if new_group_tag_form.is_valid():
            toast_message = "Group Tag created, successfully !"
            new_group_tag_form.save()
    if "group_tags_array" in request.POST:
        group_tags_str: str = request.POST['group_tags_array']
        selected_product_id: int = int(request.POST['selected_product_id'])
        group_tags_list = group_tags_str.split(',')
        #remove empty string from array
        while("" in group_tags_list):
            group_tags_list.remove("")
        if group_tags_list:
            print(selected_product_id, ' ', group_tags_list)
            Product.objects.get(id=selected_product_id).group_tags.clear()
            for name in group_tags_list:
                group_tag: GroupTag = GroupTag.objects.get(name=name)
                selected_product: Product = Product.objects.get(id=selected_product_id)
                selected_product.group_tags.add(group_tag)
        else:
            Product.objects.get(id=selected_product_id).group_tags.clear()
        
        toast_message = "Product updated, successfully !"

    context = {
        # "feed": feed,
        "feeds": feeds,
        "found_products_count": paginator.count,
        "sort_type": sort_type,
        "sorting_option_form": sorting_option_form,
        "form": paginated_form,
        "new_group_tag_form": new_group_tag_form,
        "paginator_control": paginator_control_with_products_queryset,
        "toast_message": toast_message,
        "group_tags": group_tags,
        # "feed_config_form": feed_config_form,
    }

    # export product list to .xml file; MAKES NO SENSE !!
    if "trigger-export" != "":
        print('???')
        create_final_feed_xml_file()

    return HttpResponse(template.render(context, request))
