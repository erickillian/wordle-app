from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, firstname, lastname, password, **other_fields):
        """
        Creates and saves a superuser with the given info.
        """

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') != True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.'
            )
        if other_fields.get('is_superuser') != True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
            )

        return self.create_user(email, username, firstname, lastname, password, **other_fields)

    def create_user(self, email, username, firstname, lastname, password, **other_fields):
        """
        Creates and saves a user with the given info.
        """
        if not email:
            raise ValueError(_('You must provide an email address'))

        if not username:
            raise ValueError(_('You must provide an user name'))

        email = BaseUserManager.normalize_email(email)
        user = Player(email=email, username=username,
                          firstname=firstname, lastname=lastname, **other_fields)

        user.set_password(password)
        user.save()
        return user

class Player(AbstractBaseUser, PermissionsMixin):
    """Table for keeping player information."""
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=150, blank=True)
    lastname = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'firstname', 'lastname']

    def __str__(self):
        """Display player's full name as string object representation."""
        return self.full_name

    @property
    def full_name(self):
        """The players full name, first plus last name."""
        full_name = f'{self.firstname} {self.lastname}'
        return full_name

    class Meta:
        db_table = 'player'
        verbose_name = ('player')
        verbose_name_plural = ('players')