from .models import Tag, Ingridient, Recipe, Shop_card
from users.models import Favorites
from .serializers import RecipeSerializer, TagSerializer, IngridientSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from rest_framework import status, viewsets, mixins, generics
from rest_framework.response import Response


class Recipe_get(generics.ListCreateAPIView,
                 mixins.CreateModelMixin,):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @api_view(['GET'])
    def recipe_all_get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(instance=recipes,
                                      many=True,
                                      context={'request': request})
        if serializer.is_valid():
            serializer.save()
        return self.get_paginated_response(serializer.data)


class Recipe_one(generics.ListCreateAPIView,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,):

    def get(self, request, id):
        if request.method == "GET":
            recipes = get_object_or_404(Recipe, id=id)
            serializer = RecipeSerializer(recipes,
                                          context={'request': request})
            return Response(serializer.data)

    def delete(self, request, id):
        try:
            if Recipe.objects.get(id=id, author_id=request.user.id):
                recipes = Recipe.objects.filter(id=id)
                recipes.delete()
                msg = "Пост удален!"
                return Response(msg, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            msg = "Такого поста нет, либо вы не являетесь автором поста"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        if Recipe.objects.filter(id=id).exists():
            if Recipe.objects.get(id=id, author_id=request.user.id):
                recipes = get_object_or_404(Recipe, id=id)
                serializer = RecipeSerializer(recipes, data=request.data,
                                              context={'request': request})

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
                msg = "сериализатор не валиден"
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            msg = "Вы не являетесь автором поста"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        msg = "Такого поста нет"
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required
def tags_get(request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True,)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@login_required
def tags_get_one(self, id):
    tags = Tag.objects.get(id=id)
    serializer = TagSerializer(tags)
    return JsonResponse(serializer.data, safe=False)


class IngridientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer


@api_view(['POST', 'DELETE'])
@login_required
def favorite_post(request, id):
    user = request.user
    if Recipe.objects.filter(id=id).exists():
        if request.method == 'POST':
            if Favorites.objects.filter(user_id=user.id,
                                        recipe_id=id).exists():
                msg = 'Рецепт уже в избранном'
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            Favorites.objects.create(user_id=user.id, recipe_id=id)
            msg = 'Рецепт добавлен в избранное'
            return Response(msg, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if Favorites.objects.filter(user_id=user.id,
                                        recipe_id=id).exists():
                Favorites.objects.filter(user_id=user.id,
                                         recipe_id=id).delete()
                msg = 'Рецепт удален из избранного'
                return Response(msg, status=status.HTTP_204_NO_CONTENT)
            msg = 'Рецепта не существует или уже удален из избранного'
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'POST'])
@login_required
def api_shop_cart(request, id):
    user = request.user
    if request.method == 'POST':
        if Recipe.objects.filter(id=id).exists():
            if Shop_card.objects.filter(user_id=user.id,
                                        recipe_id=id).exists():
                msg = 'Уже есть в вашем списке покупок!'
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            Shop_card.objects.create(user_id=user.id, recipe_id=id)
            msg = 'Рецепт добавлен в список покупок!'
            return Response(msg, status=status.HTTP_201_CREATED)
        msg = 'Рецепта не существует!'
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        if Shop_card.objects.filter(user_id=user.id, recipe_id=id).exists():
            Shop_card.objects.filter(user_id=user.id, recipe_id=id).delete()
            msg = 'Рецепт удален из списка покупок!'
            return Response(msg, status=status.HTTP_204_NO_CONTENT)
        msg = 'Рецепта не существует или не находится в вашем списке покупок!'
        return Response(msg, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@login_required
def load_shop_cart(request):
    pass
