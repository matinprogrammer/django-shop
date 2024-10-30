from email.policy import default

from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10)


class CouponApplyForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

