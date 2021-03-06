from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError
from django.db import models

# TODO custom auth backend
from phonenumber_field.modelfields import PhoneNumberField


class Gender:
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'
    GENDER_TYPE_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )


# TODO serializer returns uppercase values
class Grade:
    BEGINNER = 'BEGINNER'
    AMATEUR = 'AMATEUR'
    PROFESSIONAL = 'PROFESSIONAL'
    GRADE_TYPE_CHOICES = (
        (BEGINNER, 'Beginner'),
        (AMATEUR, 'Amateur'),
        (PROFESSIONAL, 'Professional')
    )


class Professional(models.Model):
    MAX_GALLERY_ITEMS = 5
    background_url = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if getattr(self, 'gallery').count() == Professional.MAX_GALLERY_ITEMS:
            raise ValidationError(
                'You can not have more than %(max_items)s gallery items',
                params={'max_items': Professional.MAX_GALLERY_ITEMS},
            )
        super(Professional, self).save(*args, **kwargs)

    # TODO configure for france?
    phone_number = PhoneNumberField()
    diploma = models.FileField(upload_to='diplomas', blank=True)
    grade = models.CharField(max_length=20,
                             choices=Grade.GRADE_TYPE_CHOICES,
                             default=Grade.AMATEUR)


class GalleryItem(models.Model):
    image_url = models.CharField(max_length=255, blank=True)
    professional = models.ForeignKey(Professional,
                                     on_delete=models.CASCADE,
                                     related_name='gallery')


class Manager(UserManager):
    def create_user(self, email=None, password=None,
                    **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class SportrotterUser(AbstractBaseUser):
    objects = Manager()
    avatar_url = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=20,
                              choices=Gender.GENDER_TYPE_CHOICES,
                              default=Gender.MALE, blank=True)
    professional = models.OneToOneField(
        Professional,
        on_delete=models.CASCADE,
        related_name='user',
        default=None,
        blank=True,
        null=True
    )
    # TODO fb access?

    USERNAME_FIELD = 'email'

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email
        # payments = None
