from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Данный email занят')
        if not username:
            raise ValueError('Имя пользователя занято')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to='images/', null=True, blank=True,
                                      default='images/avatar.jpg')
    hide_email = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def set_image_to_default(self):
        self.profile_image.delete(save=False)  # delete old image file
        self.profile_image = 'images/avatar.jpg'
        self.save()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

        def get_profile_image_filename(self):
            return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]
        # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)

    def has_module_perms(self, app_label):
        return True
