from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.datetime_safe import datetime
import uuid as uuid_util


class CustomManager(models.Manager):
    pass


class MyUserManager(BaseUserManager):

    def create_user(self, email, password):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            password=password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_util.uuid4)
    created_at = models.DateTimeField(default=datetime.now)
    deleted = models.BooleanField(default=False)

    objects = CustomManager()

    class Meta:
        abstract = True

    abstract = True

    def delete(self, **kwargs):
        self.deleted = True
        self.save()


class Car(BaseModel):
    maker = models.CharField(max_length=32, null=False, blank=False)
    color = models.CharField(max_length=32, null=False, blank=False)
    license_plate = models.CharField(max_length=32, null=False, blank=False)

    def __str__(self):
        return f"{self.license_plate}"


class User(AbstractBaseUser, BaseModel):
    email = models.EmailField(verbose_name='email', max_length=128, unique=True, null=False, blank=False)
    password = models.CharField(max_length=256, null=False, blank=False)
    last_name = models.CharField(max_length=32, null=False, blank=False, default="admin")
    first_name = models.CharField(max_length=32, null=False, blank=False, default="admin")
    birth = models.DateField(null=False, blank=False, default=datetime.now)
    rating = models.FloatField(null=True, blank=True, validators=[
            MaxValueValidator(5.0),
            MinValueValidator(0.0)
        ])
    phone_number = models.CharField(max_length=32, null=False, blank=False, default="00000000")
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    car = models.ManyToManyField(Car, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f"{self.first_name}-{self.last_name}-{self.uuid}"


class Route(BaseModel):
    starting_location = models.CharField(max_length=256, null=False, blank=False)
    end_location = models.CharField(max_length=256, null=False, blank=False)
    starting_time = models.DateTimeField(null=False, blank=False)
    contribution = models.FloatField(null=True, blank=True, default=0.0)
    available_seats = models.IntegerField(null=False, blank=False)

    passenger = models.ManyToManyField(User, related_name="passenger")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car")

    def __str__(self):
        return f"{self.car}-{self.starting_location}-{self.end_location}"


class CheckIn(BaseModel):
    checkin_time = models.DateTimeField(null=False, blank=False)

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="route")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checkin_user")

    def __str__(self):
        return f"{self.checkin_time}-{self.route}"
