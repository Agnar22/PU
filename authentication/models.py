from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


class ProfileManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, phone_number):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.PositiveIntegerField()
    is_admin = models.BooleanField(default=False)
    profile_picture = ProcessedImageField(upload_to='apartments/',
                                          processors=[ResizeToFit(300, 300, False)],
                                          format='JPEG',
                                          options={'quality': 85}, null=True, blank=True)

    objects = ProfileManager()

    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)
    vote_sum = models.PositiveIntegerField(default=0)
    vote_amount = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def update_rating(self, new_rating):
        self.vote_amount += 1
        self.vote_sum += abs(new_rating)
        self.rating = round(self.vote_sum / self.vote_amount)

    def save(self, *args, **kwargs):
        if not self.first_name:
            self.profile_picture = ''
        super().save(*args, **kwargs)

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
