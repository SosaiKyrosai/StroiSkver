from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordResetForm
from django import forms
from django.contrib.auth import authenticate, login
from order.models import Order
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
import random
import string


class ResetPasswordRequestForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')


class ResetPasswordConfirmForm(forms.Form):
    control_response = forms.CharField(label='Ответ на контрольный вопрос')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин:", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль:", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


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
        fields = ['first_name', 'last_name', 'email', 'username']

    photo = forms.ImageField(required=False)
    phone_number = forms.CharField(max_length=12, required=False)
    city = forms.CharField(max_length=255, required=False)
    street = forms.CharField(max_length=255, required=False)
    house_number = forms.CharField(max_length=10, required=False)
    apartment_number = forms.CharField(max_length=10, required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.photo = self.cleaned_data['photo']
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
        fields = ("first_name", "last_name", "email", "username")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("photo", "phone_number", "city", "street", "house_number", "apartment_number")


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['security_question', 'control_response']


@login_required
@transaction.atomic
def profile_edit(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
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
            user = form.save()
            login(request, user)
            return redirect('add_question')  # Перенаправление после успешной регистрации
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
    user = request.user
    profile = Profile.objects.get(user=user)
    orders = Order.objects.filter(user=user).order_by('-order_date')[:3]  # Получение последних 3 заказов пользователя
    has_more_orders = Order.objects.filter(user=user).count() > 3  # Проверка наличия больше заказов
    context = {
        'user': user,
        'profile': profile,
        'orders': orders,
        'has_more_orders': has_more_orders
    }
    return render(request, 'profile.html', context)


@login_required
def add_question(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            security_question = form.cleaned_data['security_question']
            control_response = form.cleaned_data['control_response']

            # Дополнительная валидация для поля control_response
            if ' ' in control_response:
                form.add_error('control_response', 'Поле должно содержать только одно слово.')
            else:
                if profile:
                    # Обновление существующего объекта Profile
                    profile.security_question = security_question
                    profile.control_response = control_response

                    profile.save()
                else:
                    # Создание нового объекта Profile
                    profile = Profile.objects.create(
                        user=request.user,
                        security_question=security_question,
                        control_response=control_response
                    )

                # Дальнейшая обработка данных

                return redirect('home')  # Перенаправление на страницу Home

    else:
        if profile:
            # Заполнение формы данными из существующего объекта Profile
            form = AddQuestionForm(initial={
                'security_question': profile.security_question,
                'control_response': profile.control_response
            })
        else:
            form = AddQuestionForm()

    return render(request, 'add_question.html', {'form': form})


def reset_password_request(request):
    if request.method == 'POST':
        form = ResetPasswordRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                profile = Profile.objects.get(user=user)
                security_question = profile.security_question
                # Перенаправление на страницу с контрольным вопросом
                return redirect('reset_password_confirm', username=username)
            except User.DoesNotExist:
                messages.error(request, 'Пользователь с таким именем не найден')
            except Profile.DoesNotExist:
                messages.error(request, 'Пользователь с таким именем не найден')
    else:
        form = ResetPasswordRequestForm()

    return render(request, 'password_reset_request.html', {'form': form})

def reset_password_confirm(request, username):
    user = get_object_or_404(User, username=username)  # Получение пользователя по имени пользователя
    profile = get_object_or_404(Profile, user=user)  # Получение профиля пользователя

    if request.method == 'POST':
        form = ResetPasswordConfirmForm(request.POST)
        if form.is_valid():
            control_response = form.cleaned_data['control_response']
            # Проверка правильности ответа на контрольный вопрос
            if control_response == profile.control_response:
                # Генерация нового пароля
                new_password = generate_random_password()
                # Обновление пароля пользователя
                user.set_password(new_password)
                user.save()
                # Отображение нового пароля на странице
                return render(request, 'password_reset_success.html', {'new_password': new_password})
            else:
                messages.error(request, 'Неверный ответ на контрольный вопрос')
    else:
        form = ResetPasswordConfirmForm()

    return render(request, 'password_reset_confirm.html', {'form': form, 'security_question': profile.security_question})


def password_reset_success(request):
    # Логика для страницы успешного сброса пароля
    return render(request, 'password_reset_success.html')


def generate_random_password():
    # Генерация случайного пароля из 8 символов
    characters = string.ascii_letters + string.digits
    random_password = ''.join(random.choice(characters) for _ in range(8))
    return random_password


def password_reset_success(request):
    return render(request, 'password_reset_success.html')