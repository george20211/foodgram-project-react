from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Tag(models.Model):
    name = models.CharField(
        max_length=200)

    color = models.CharField(
        max_length=7,
        unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Ingridient(models.Model):
    name = models.CharField(max_length=200, blank=True, null=False)
    measurement_unit = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts")
    name = models.CharField(max_length=200, blank=True, null=False)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    text = models.TextField(max_length=100)
    pub_date = models.DateTimeField("date published",
                                    auto_now_add=True)
    ingredients = models.ManyToManyField(
        'Ingridient',
        related_name='ingredienting'
    )
    tags = models.ManyToManyField('Tag', related_name='m2m_tags')
    cooking_time = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['-pub_date', ]

    def __str__(self):
        return ('__all__').format(**self.__dict__)


class Shop_card(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shop_recipe',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_field')
        ]


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
    )


class TagsInRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
