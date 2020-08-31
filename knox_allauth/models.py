import random
import string

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, name=None, phone=None,**extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        site_id = name + ''.join(random.SystemRandom()
                            .choice(string.ascii_letters + string.digits) 
                            for _ in range(6))
        if_exist_already = CustomUser.objects.filter(site_id=site_id).count() > 0
        print(if_exist_already)
        while if_exist_already:
            print(if_exist_already)
            site_id = name + ''.join(random.SystemRandom()
                                .choice(string.ascii_letters + string.digits) 
                                for _ in range(6))
            if_exist_already = CustomUser.objects.filter(site_id=site_id).count() > 0
        user = self.model(email=email, name=name, phone=phone, site_id=site_id,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, name, phone, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, name, phone, **extra_fields)

    def create_superuser(self, email, password, name, phone, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, name, phone,**extra_fields)

def upload_path(instance, filname):
    return '/'.join(['pictures/', str(instance.site_id)+'.'+filname.split('.')[-1]])

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)
    site_id = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    bio = models.CharField(max_length=500)
    rating = models.DecimalField(default=0, decimal_places=1, max_digits=2,
                                    validators=[MaxValueValidator(5),MinValueValidator(1)])
    members = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    earning = models.IntegerField(default=0)
    profession = models.CharField(max_length=100)
    location = models.CharField(max_length=50) #Name of city, change it to location maybe?
    member_since = models.DateTimeField(default=timezone.now, null=True) #Do something about it
    picture = models.ImageField(upload_to=upload_path, null=False, blank=False, default='pictures/profile.png')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']
    def __str__(self):
        return f"email={self.email} name={self.name}"

    objects = UserManager()

