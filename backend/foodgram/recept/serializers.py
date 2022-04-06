from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import Favorites
from drf_extra_fields.fields import Base64ImageField
from .models import (Tag, Ingridient, Recipe, TagsInRecipe,
                     Shop_card, IngredientsRecipe)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('__all__')


class TagInRecipeSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = '__all__'


class IngridientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingridient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_name(self, obj):
        ing = Ingridient.objects.get(id=obj.ingredient.id)
        return str(ing)

    def get_id(self, obj):
        return obj.ingredient.id

    def get_amount(self, obj):
        return obj.amount


class RecipeSerializer(ModelSerializer):
    tags = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context['request']
        user = request.user.id
        return Favorites.objects.filter(user_id=user).exists()

    def get_is_in_shopping_cart(self, obj):
        return Shop_card.objects.filter(recipe_id=obj.id).exists()

    def get_tags(self, obj):
        objects = TagsInRecipe.objects.filter(recipe_id=obj.id)
        all_obj = []
        for x in objects:
            obj = Tag.objects.filter(id=x.tag_id)
            all_obj += obj
        return TagSerializer(all_obj, many=True).data

    def get_author(self, obj):
        from users.models import User as polzovatel
        author = polzovatel.objects.filter(id=obj.author.id)
        return AuthorSerializer(author, many=True).data

    def get_ingredients(self, obj):
        objects = IngredientsRecipe.objects.filter(recipe_id=obj.id)
        return IngridientSerializer(objects, many=True).data

    def get_ingredients_amount(self, ingredients, recipe, data):
        tags = data['tags']
        for tag_id in tags:
            recipe.tags.add(get_object_or_404(Tag, pk=tag_id))
        for ingredient in ingredients:
            ingredients_amount = IngredientsRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
            ingredients_amount.save()

    def validate(self, data):
        print(self.__dict__, 00000000000000000000000)
        request = self.context['request']
        ingredients = request.data['ingredients']
        tags = request.data['tags']
        request.data['author_id'] = request.user.id
        for ingredients_num in ingredients:
            if Ingridient.objects.filter(
                    id=ingredients_num.get('id')
                                        ).exists():
                if ingredients_num.get('amount') <= 0:
                    raise serializers.ValidationError("не может быть 0")
            else:
                raise serializers.ValidationError("Ингридиента нет")
        for tags in tags:
            if Tag.objects.filter(id=tags).exists():
                pass
            else:
                raise serializers.ValidationError("Тэга нет в базе")
        data = request.data
        return data

    def create(self, validated_data):
        tags_set = validated_data.pop('tags')
        ingredient_set = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
                **validated_data
            )

        for ingredient in ingredient_set:
            IngredientsRecipe.objects.create(
                recipe=recipe,
                ingredient=Ingridient.objects.get(id=ingredient['id']),
                amount=ingredient['amount'],

            )
            print(Recipe.__doc__)
        for tags in tags_set:
            TagsInRecipe.objects.create(
                recipe=recipe,
                tag=Tag.objects.get(id=tags)
            )
        return recipe

    def update(self, instance, validated_data):
        context = self.context['request']
        validated_data.pop('ingredients')
        tags_set = context.data['tags']
        recipe = instance
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        instance.tags.set(tags_set)
        IngredientsRecipe.objects.filter(recipe=instance).delete()
        ingredients_req = context.data['ingredients']
        for ingredient in ingredients_req:
            ingredient_model = Ingridient.objects.get(id=ingredient['id'])
            IngredientsRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient_model,
                amount=ingredient['amount'],
            )
        return instance


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        from users.models import User as users
        model = users
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        return obj.user.follower.filter(author=obj.author).exists()
