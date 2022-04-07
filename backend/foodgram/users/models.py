from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
import jwt
from .settings import SECRET_KEY
from recept.models import Recipe
from django.conf import settings
from recept.models import Recipe

#User = settings.AUTH_USER_MODEL


class MyUserManager(BaseUserManager):
    def _create_user(self, email, username, password,
                     first_name, last_name, is_active, is_superuser):
        if not first_name:
            raise ValueError("нет имя")
        if not last_name:
            raise ValueError("нет фамилии")
        if not email:
            raise ValueError("нет еmail")
        if username == 'me':
            raise ValueError("имя пользователя запрещено")
        if not username:
            raise ValueError("нет логина")
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_superuser = is_superuser
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password, first_name, last_name):
        is_active = True
        is_superuser = False
        return self._create_user(email, username, password,
                                 first_name, last_name, is_active,
                                 is_superuser)

    def create_superuser(self, email, username,
                         password, first_name, last_name):
        return self._create_user(email, username, password,
                                 first_name, last_name, is_active=1,
                                 is_superuser=1)


class User(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True, unique=True,
                          verbose_name='id',)
    username = models.CharField(max_length=50, unique=True,
                                verbose_name='ник',)
    email = models.EmailField(max_length=100, unique=True,
                              verbose_name='почта',)
    is_active = models.BooleanField(default=True,
                                    verbose_name='активность',)
    is_staff = models.BooleanField(default=False,
                                   verbose_name='staff',)
    first_name = models.CharField(max_length=50, unique=False,
                                  verbose_name='имя',)
    last_name = models.CharField(max_length=50, unique=False,
                                 verbose_name='фамилия',)
    is_subscribed = models.BooleanField(default=False,
                                        verbose_name='подписан или нет',)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, SECRET_KEY, algorithm='HS256')

        return token
    
    def __str__(self):
        return ('__all__').format(**self.__dict__)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower",
                             verbose_name='подписчик',)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following",
                               verbose_name='автор',)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_field')
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.user, self.author


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='подписчик',)
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE,
                                  related_name="favorites",
                                  verbose_name='рецепт',)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_field')
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return self.user, self.recipe
