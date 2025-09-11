from django import forms
from shop.models import CustomerProfile, Address # assuming you have a Customer model

class CustomerRegisterForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['customer_name', 'customer_email', 'phone_number']  # adjust fields as per your model
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }

class CustomerForm(forms.Form):
    # MyUser fields
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    # CustomerProfile fields
    phone_number = forms.CharField(max_length=15, required=False)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line', 'city', 'postal_code', 'country', 'address_type', 'is_default']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  # <-- make all optional