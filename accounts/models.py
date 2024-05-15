from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number, username, password=None):
        if not email:
            raise ValueError('User must have email')
        
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            phone_number = phone_number,
            user_name = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, password, phone_number, username):
        user  = self.create_user(
            first_name, last_name, self.normalize_email(email), phone_number, username, password)

        user.is_admin = True
        user.is_staff = True
        user.is_active= True
        user.is_superadmin = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    first_name      = models.CharField(max_length=70)
    last_name       = models.CharField(max_length=70)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)
    username        = models.CharField(max_length = 100, blank = True)

    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superadmin   = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = MyAccountManager()

    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

