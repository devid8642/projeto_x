from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
from utils.image import resize_image
from solo.models import SingletonModel


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    profile_photo = models.ImageField(
        'Foto de perfil', blank=True, null=True,
        upload_to='profiles_photos/'
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def save(self, *args, **kwargs):
        saved = super().save(*args, **kwargs)

        if self.profile_photo:
            try:
                resize_image(self.profile_photo, new_width=208)
            except FileNotFoundError:
                pass
        
        return saved

    def __str__(self):
        return f'User {self.id} - {self.email}'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'users'
        ordering = ['id']


class ProjectsDate(SingletonModel):
    start_date = models.DateTimeField('Data inicial', null=True)
    end_date = models.DateTimeField('Data final', null=True)

    def __str__(self):
        return f'Prazo: {self.start_date} - {self.end_date}'

    class Meta:
        db_table = 'prazo'
        verbose_name = 'prazo'
