from urllib import request
from django.forms import ValidationError
from .models import Recipe, User, Follow, MyUserManager
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class FollowersSerializer(serializers.ModelSerializer):
    author_id = serializers.StringRelatedField()
    user_id = serializers.StringRelatedField()
    model = Follow
    fields = ['__all__']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.StringRelatedField()
    username = serializers.StringRelatedField()
    first_name = serializers.StringRelatedField()
    last_name = serializers.StringRelatedField()

    class Meta:
        model = MyUserManager
        fields = ['email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUserManager(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserChangePassSerializer(serializers.ModelSerializer):
    def validate(self, obj):
        user = User.objects.get(username=request.user)
        if user.password == obj.current_password:
            user.set_password(obj.new_password)
            user.save()
            return obj
        else:
            raise ValidationError("Старый пароль не совпал")


class RecipeSerializerForFollow(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowListSerializer(ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipe = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes_count', 'recipe',
        )

    def get_recipe(self, obj):
        data = Recipe.objects.filter(author=obj.author)
        return RecipeSerializerForFollow(data, many=True).data

    def get_is_subscribed(self, obj):
        return obj.user.follower.filter(author=obj.author).exists()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class IamSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        return obj.user.follower.filter(author=obj.author).exists()
