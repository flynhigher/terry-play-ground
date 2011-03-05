from django import forms
from django.utils.translation import ugettext_lazy as _

from product.models import Product, Price

class ProductForm(forms.ModelForm):
#    
#    slug = forms.SlugField(max_length=20,
#        help_text = _("a short version of the name consisting only of letters, numbers, underscores and hyphens."),
#        error_message = _("This value must contain only letters, numbers, underscores and hyphens."))
            
    def clean_slug(self):
        reserved_slugs = ["your_product"]
        if self.cleaned_data["slug"] in reserved_slugs:
            raise forms.ValidationError(_("The slug you've chosen is reserved for internal use."))
        if Product.objects.filter(slug__iexact=self.cleaned_data["slug"]).count() > 0:
            raise forms.ValidationError(_("A product already exists with that slug."))
        return self.cleaned_data["slug"].lower()
    
    def clean_name(self):
        if Product.objects.filter(name__iexact=self.cleaned_data["name"]).count() > 0:
            raise forms.ValidationError(_("A product already exists with that name."))
        return self.cleaned_data["name"]
    
    class Meta:
        model = Product
#        fields = ('name', 'slug', 'description', 'tags')


# @@@ is this the right approach, to have two forms where creation and update fields differ?

class ProductUpdateForm(forms.ModelForm):
    def clean_name(self):
        if Product.objects.filter(name__iexact=self.cleaned_data["name"]).count() > 0:
            if self.cleaned_data["name"] == self.instance.name:
                pass # same instance
            else:
                raise forms.ValidationError(_("A product already exists with that name."))
        return self.cleaned_data["name"]
    
    class Meta:
        model = Product
#        fields = ('name', 'description', 'tags')


class PriceForm(forms.ModelForm):
    
    class Meta:
        model = Price
#        fields = ('title', 'body', 'tags')

class PricePostForm(forms.ModelForm):
    
    class Meta:
        model = Price
#        fields = ('title', 'body', 'tags')
