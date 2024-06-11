from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _ 

''' gettext_lazy Means if application is translated into different languages, 
    this string will be translated accordingly. ''' 



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)       # is_active False for Email Verification 
        user = self.model(email=email, **extra_fields)    # Instead of username, here we used email pass none here also need *** auth_email.py 
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        ''' These are optional '''
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        ''' These are optional '''
        return self.create_user(email, password, **extra_fields)



class AppUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  
    ''' REQUIRED_FIELDS empty means there no extra fields required for creating a user.
        If we pass REQUIRED_FIELDS = ['first_name'] need first_name when
        no need to pass 'email' here
    '''
    
    activation_code = models.CharField(max_length=50, blank=True, null=True)
    password_reset_code = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    credit = models.IntegerField(default=0)
    
    
    # Remove related_name for groups and user_permissions
    # Best uses is not using, where dosen't have mulple user role
    '''
    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission)
    '''
    
    objects = UserManager()

    def activate(self):
        self.is_active = True
        self.activation_code = ''
        self.save()
    
    def save(self, *args, **kwargs):        # For email Lowercase
        if self.email:
            self.email.lower()
        super(AppUser, self).save(*args, **kwargs)


'''
Alternate Way :

class AppUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    
    # Remove related_name for groups and user_permissions
    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission)
    objects = UserManager()

    def activate(self):
        self.is_active = True
        self.activation_code = ''
        self.save()

    def save(self, *args, **kwargs):
        # For email lowercase
        self.email = self.email.lower()
        super(AppUser, self).save(*args, **kwargs)

class Customer(models.Model):
    user_profile = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    activation_code = models.CharField(max_length=50, blank=True, null=True)
    password_reset_code = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    credit = models.IntegerField(default=0)

    def activate(self):
        # Call the activate method of the associated AppUser
        self.user_profile.activate()
'''
