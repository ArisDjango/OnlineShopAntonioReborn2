from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]
# PRODUCT_QUANTITY_CHOICES = [(1)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int,
                                # widget=forms.NumberInput(attrs={ 'max': 100, 'min': 1})
                                )
    # quantity = forms.IntegerField(MinValueValidator(1))
    override = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)