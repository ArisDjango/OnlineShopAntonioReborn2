from django import forms
# from localflavor.id_.forms import IDPostCodeField
from localflavor.us.forms import USZipCodeField
from .models import Order

class OrderCreateForm(forms.ModelForm):
    postal_code = USZipCodeField()
    # postal_code = IDPostCodeField()
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']