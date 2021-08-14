from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin


# Global variables to store user role
ROLE_STUDENT = 's'
ROLE_TEACHER = 't'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create user by email and password"""
        if not email:
            raise ValueError("user must have an email")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create superuser by email and password"""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.role = ROLE_TEACHER
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
        User model to save user by email instead of username
    """

    ROLE_CHOICES = (
        (ROLE_STUDENT, 'student'),
        (ROLE_TEACHER, 'teacher'),
    )

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(choices=ROLE_CHOICES, default=ROLE_STUDENT,
                            max_length=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
