from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'birth_date', 'picture')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'phone_number',
            'first_name',
            'last_name',
            'birth_date',
            'picture',
            'is_active',
            'is_admin',
            'last_login'
        )

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        min_length=11,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'data-toggle': 'password',
            }
        )
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'data-toggle': 'password',
            }
        )
    )

    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'birth_date', 'picture')
        widgets = {
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'birth_date': forms.DateInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'picture': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match')
        return password2

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('Phone number is taken')
        return phone_number

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()

