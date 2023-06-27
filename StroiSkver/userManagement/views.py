from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm
from django import forms
from django.contrib.auth import authenticate, login


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CustomUserCreationForm(UserCreationForm):
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Удаление help_text
        for field_name, field in self.fields.items():
            field.help_text = None

        # Задание error_messages на русском
        self.fields['username'].error_messages = {'required': 'Введите имя пользователя.', 'unique': 'Пользователь с таким именем уже существует.'}
        self.fields['password1'].error_messages = {'required': 'Введите пароль.'}
        self.fields['password2'].error_messages = {'required': 'Введите подтверждение пароля.', 'password_mismatch': 'Пароли не совпадают.'}

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.fields['password2'].error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


class ProfileEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    phone_number = forms.CharField(max_length=12, required=False)
    city = forms.CharField(max_length=255, required=False)
    street = forms.CharField(max_length=255, required=False)
    house_number = forms.CharField(max_length=10, required=False)
    apartment_number = forms.CharField(max_length=10, required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone_number = self.cleaned_data['phone_number']
        profile.city = self.cleaned_data['city']
        profile.street = self.cleaned_data['street']
        profile.house_number = self.cleaned_data['house_number']
        profile.apartment_number = self.cleaned_data['apartment_number']
        if commit:
            user.save()
            profile.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("photo", "phone_number", "city", "street", "house_number", "apartment_number")


@login_required
@transaction.atomic
def profile_edit(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, "profile_edit.html", {"u_form":user_form, "p_form": user_profile_form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправление после успешной регистрации
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправление после успешной авторизации
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def profile(request):
    user = request.user  # Получение текущего пользователя
    profile = Profile.objects.get(user=user)  # Получение профиля пользователя
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'profile.html', context)