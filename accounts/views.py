from distutils.log import fatal

from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import UserLoginForm, UserRegisterForm, VerifyCodeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User, OtpCode
from random import randint
from utils import send_otp_code


USER_REGISTER_SESSION_KEY = 'user_registration_info'

# TODO: clear  code
# TODO: write test
class UserLoginView(View):
    template_name = 'accounts/user_login.html'
    form_class = UserLoginForm

    def get(self, request):
        return render(request, self.template_name, context={
            'form': self.form_class,
        })

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(phone_number=cd['phone_number'], password=cd['password'])
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in', 'success')
                return redirect('home:home')
            messages.error(request, 'Invalid username or password', 'danger')

        return render(request, self.template_name, context={
            'form': form,
        })


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are now logged out', 'success')
        return redirect('home:home')


class UserRegisterView(View):
    template_name = 'accounts/user_register.html'
    form_class = UserRegisterForm

    def get(self, request):
        return render(request, self.template_name, context={
            'form': self.form_class,
        })

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = randint(100000, 999999)
            # send_otp_code(phone_number=form.cleaned_data['phone_number'], code=random_code)
            print(random_code)
            OtpCode.objects.create(
                phone_number=form.cleaned_data['phone_number'],
                code=random_code,
            )
            request.session[USER_REGISTER_SESSION_KEY] = {
                'phone_number': form.cleaned_data['phone_number'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'birth_date': form.cleaned_data['birth_date'],
                'password': form.cleaned_data['password2'],
            }

            messages.success(request, 'your code send it', 'success')
            return redirect('accounts:user_register_verify_code')
        messages.error(request, 'the register have error', 'danger')
        return render(request, self.template_name, context={
            'form': form,
        })

class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'accounts/user_register_verify_code.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, context={
            'form': form,
        })

    # TODO: overwrite save method of user
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user_session = request.session[USER_REGISTER_SESSION_KEY]
            code_instance = OtpCode.objects.filter(phone_number=user_session['phone_number']).last()

            if code_instance.code == code:
                user = User.objects.create(
                    phone_number=user_session['phone_number'],
                    first_name=user_session['first_name'],
                    last_name=user_session['last_name'],
                    birth_date=user_session['birth_date'],
                )
                user.is_active = True
                user.set_password(user_session['password'])
                user.save()
                code_instance.delete()
                login(request, user)
                messages.success(request, 'Your code has been sent successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'Your code have error', 'danger')
            return render(request, self.template_name, context={
                'form': self.form_class,
            })





