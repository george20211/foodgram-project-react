from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, IngredientInRecipe,
                     Purchase, Recipe, Tag)


class RecipeIngredientAdmin(admin.TabularInline):
    model = IngredientInRecipe

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('^name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'favorited')
    list_filter = ('author', 'name', 'tags')
    exclude = ('ingredients',)

    def favorited(self, obj):
        return Favorite.objects.filter(recipe=obj).count()
    
    inlines = [
        RecipeIngredientAdmin,
    ]

    favorited.short_description = 'В избранном'


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')

# Редактирование количества ингридиентов
# перенес на страницу рецептов
"""class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount')"""

admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Follow, SubscriptionAdmin)
#admin.site.register(IngredientInRecipe)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
