from django import forms
from access.models import User
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


# Hacer una clase de formulario para registrar un usuario con UserCreationForm
class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'The email address is already in use.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        # Validar que las contraseñas coincidan
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'The passwords do not match.')
        return password2

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        return cleaned_data

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.date_joined = timezone.now()
        if commit:
            user.save()
        return user

#     def save(self):
#         email = self.cleaned_data['email']
#         password = self.cleaned_data['password']
#         first_name = self.cleaned_data['first_name']
#         last_name = self.cleaned_data['last_name']
#         date_joined = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
#         user = User.objects.create_user(
#             username=email, email=email, password=password,
#             first_name=first_name, last_name=last_name, date_joined=date_joined)
#         return user


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']
