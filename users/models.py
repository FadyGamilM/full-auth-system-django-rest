from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email, first_name, last_name and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            **kwargs
        )

        # hash the password
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email, password.
        """
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )
        #! 2 flags for the super user
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    # is_Active will be set by djoser as false because we will make the user go and activate his/her email first
    # but i am leaving it as true here as when i run `createsuperuser` i will need this user to be active so i can login at the admin panel
    is_active = models.BooleanField(default=True)
    # this will give this user the ability to login in into the admin panel
    is_admin = models.BooleanField(default=False)
    # this will give this user the permission to edit things in the admin panel
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    #! additional fields rather than the username_field to be required in the registeration process
    REQUIRED_FIELDS = ["first_name", 'last_name']

    def __str__(self):
        return self.email
