from django import forms
from .models import Contact, Address, BankAccount

from django import forms
from .models import Contact, Address, BankAccount

class UnifiedProfileForm(forms.ModelForm):
    """Unified form to update Contact, Address, and BankAccount in one form."""
    
    # Address Fields
    address_type = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Billing, Home, etc."})
    )
    address_line_1 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    address_line_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    postal_code = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    country = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

    # Bank Account Fields
    account_holder = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    iban = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    bic = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Contact
        fields = ["email", "first_name", "last_name", "company_name", "phone_number"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        """Pre-fill the form with existing data from Contact, Address, and BankAccount."""
        user = kwargs.pop("user", None)  # Pass user manually
        super().__init__(*args, **kwargs)

        if user:
            # Prefill Address if available
            address = Address.objects.filter(contact=user).first()
            if address:
                self.fields["address_type"].initial = address.type
                self.fields["address_line_1"].initial = address.address_line_1
                self.fields["address_line_2"].initial = address.address_line_2
                self.fields["postal_code"].initial = address.postal_code
                self.fields["city"].initial = address.city
                self.fields["country"].initial = address.country

            # Prefill BankAccount if available
            bank_account = BankAccount.objects.filter(contact=user).first()
            if bank_account:
                self.fields["account_holder"].initial = bank_account.account_holder
                self.fields["iban"].initial = bank_account.iban
                self.fields["bic"].initial = bank_account.bic

    def save(self, commit=True, user=None):
        """Save Contact, Address, and BankAccount together."""
        contact = super().save(commit=False)  # Save Contact model fields
        if commit:
            contact.save()

        # Save Address
        address, _ = Address.objects.get_or_create(contact=contact)
        address.type = self.cleaned_data["address_type"]
        address.address_line_1 = self.cleaned_data["address_line_1"]
        address.address_line_2 = self.cleaned_data["address_line_2"]
        address.postal_code = self.cleaned_data["postal_code"]
        address.city = self.cleaned_data["city"]
        address.country = self.cleaned_data["country"]
        address.save()

        # Save BankAccount
        bank_account, _ = BankAccount.objects.get_or_create(contact=contact)
        bank_account.account_holder = self.cleaned_data["account_holder"]
        bank_account.iban = self.cleaned_data["iban"]
        bank_account.bic = self.cleaned_data["bic"]
        bank_account.save()

        return contact
