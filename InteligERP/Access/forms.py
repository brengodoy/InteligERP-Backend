from django import forms
from django.contrib.auth.models import User
from datetime import datetime


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        # la fecha se manda desde el front? o puede quedar así?:
        date_joined = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name, date_joined=date_joined)
        return user


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("User does not exist.")

        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise forms.ValidationError("Incorrect password.")

    def save(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.get(email=email)
        return user
