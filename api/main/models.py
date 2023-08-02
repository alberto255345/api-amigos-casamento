import uuid
from distutils.command.upload import upload
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Prepare UserManager
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('category', '1')
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('category', '1')

        if extra_fields.get('category') is not '1':
            raise ValueError('A category must be 1')

        return self._create_user(email, password, **extra_fields)

# # Type of User
# class categoryUser(models.Model):
#     category = models.CharField('categoria', max_length=255, blank=True, null=True)

#     def __str__(self):
#         return self.category

# Create user
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Nome', max_length=255, blank=True, null=True)
    email = models.EmailField('email do usuário', unique=True)
    created_at = models.DateTimeField('criado as', auto_now_add=True)
    updated_at = models.DateTimeField('alterado as', auto_now=True)
    # category = models.ForeignKey(categoryUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Definição se o usuário está ativo',
    )

    # Altere o related_name para evitar conflitos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )


    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.email