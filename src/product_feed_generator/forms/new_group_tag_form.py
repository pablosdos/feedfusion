from django import forms
from product_feed_generator.models import GroupTag

class NewGroupTagForm(forms.ModelForm):
  class Meta:
    model = GroupTag
    fields = '__all__'