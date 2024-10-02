from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


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


