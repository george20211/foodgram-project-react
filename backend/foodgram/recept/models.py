from django.db import models
from django.conf import settings
from django.forms import ValidationError

User = settings.AUTH_USER_MODEL

class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='название тега',)

    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='цвет',
    )
    slug = models.SlugField(unique=True,
                            verbose_name='слаг',)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingridient(models.Model):
    name = models.CharField(max_length=200, blank=True, null=False,
                            verbose_name='название',)
    measurement_unit = models.CharField(max_length=50, blank=True, null=True,
                                        verbose_name='ед. измерения',)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return (f'{self.name}, {self.measurement_unit}').format(**self.__dict__)


class Recipe(models.Model):

    def validate_null(value):
        if value <= 0:
            raise ValidationError('значение не может быть меньше 1')

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts",
                               verbose_name='автор',)
    name = models.CharField(max_length=200, blank=True, null=False,
                            verbose_name='название',)
    image = models.ImageField(upload_to='posts/', blank=True, null=True,
                              verbose_name='фото',)
    text = models.TextField(max_length=100,
                            verbose_name='текст',)
    pub_date = models.DateTimeField("date published",
                                    auto_now_add=True,)
    ingredients = models.ManyToManyField(
        'Ingridient',
        related_name='ingredienting',
        verbose_name='ингридиенты',
    )
    tags = models.ManyToManyField('Tag', related_name='m2m_tags',
                                  verbose_name='тэги',)
    cooking_time = models.PositiveSmallIntegerField(validators=[validate_null],
                                                    verbose_name='время',)

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        #return ('__all__').format(**self.__dict__)
        return self.name


class Shop_card(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_recipe',
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shop_recipe',
        verbose_name='рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_field')
        ]
        verbose_name = 'корзина покупателя'
        verbose_name_plural = 'корзины покупателей'
    
    def __str__(self):
        return self.user


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )
    amount = models.PositiveIntegerField(verbose_name='кол-во',)

    class Meta:
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецептах'

    def __str__(self):
        return self.ingredient, self.recipe, self.amount

class TagsInRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='рецепт',)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                            verbose_name='тэг',)

    class Meta:
        verbose_name = 'Тэг в рецепте'
        verbose_name_plural = 'Тэги в рецептах'

    def __str__(self):
        return self.tag, self.recipe
