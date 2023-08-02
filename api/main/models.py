import uuid
from distutils.command.upload import upload
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, User as UserMaster
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
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)

# Create user
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Nome', max_length=255, blank=True, null=True)
    email = models.EmailField('email do usuário', unique=True)
    created_at = models.DateTimeField('criado as', auto_now_add=True)
    updated_at = models.DateTimeField('alterado as', auto_now=True)
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
    
class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    is_approved = models.BooleanField(
        'approved',
        default=False,
        help_text='Definição se a foto está aprovada',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def approve(self):
        self.is_approved = True
        self.save()

class Like(models.Model):
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def like_photo(cls, user, photo):
        like, created = cls.objects.get_or_create(user=user, photo=photo)
        return like

class Comment(models.Model):
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_comment(cls, user, photo, text):
        comment = cls(user=user, photo=photo, text=text)
        comment.save()
        return comment