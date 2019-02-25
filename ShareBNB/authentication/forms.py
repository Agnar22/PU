from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = "email"
        self.fields['email'].widget.attrs['placeholder'] = "email"
        self.fields['first_name'].widget.attrs['autocomplete'] = "given-name"
        self.fields['last_name'].widget.attrs['autocomplete'] = "family-name"
        self.fields['phone_number'].widget.attrs['autocomplete'] = "tel-national"
        self.fields['password'].widget.attrs['autocomplete'] = "new-password"
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
