from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.conf import settings
from .forms import LoginForm, RegisterForm


class LoginFormView(View):

    template_name = 'authentication/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    
        # Refreshes the login form if not correct
        return render(request, self.template_name, {'form': form})


class RegisterFormView(View):
    form_class = RegisterForm
    template_name = 'authentication/register.html'

    # display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print(form.cleaned_data['email'])
            
            # Cleaned (normalized) data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Returns User objects if credentials are correct
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)  # User is logged in
                    return redirect('/')

        return render(request, self.template_name, {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/')

