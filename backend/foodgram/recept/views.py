from .models import (Tag, Ingridient, Recipe, Shop_card,
                     IngredientsRecipe)
from users.models import Favorites
from .serializers import RecipeSerializer, TagSerializer, IngridientSerializer
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from rest_framework import status, viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class Recipe_get(generics.ListCreateAPIView,
                 mixins.CreateModelMixin,):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination


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
        if Favorites.objects.filter(user_id=user.id,
                                    recipe_id=id).exists():
            if request.method == 'DELETE':
                Favorites.objects.filter(user_id=user.id,
                                         recipe_id=id).delete()
                msg = 'Рецепт удален из избранного'
                return Response(msg, status=status.HTTP_204_NO_CONTENT)
            if request.method == 'POST':
                msg = 'Рецепт уже в избранном'
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        Favorites.objects.create(user_id=user.id, recipe_id=id)
        msg = 'Рецепт добавлен в избранное'
        return Response(msg, status=status.HTTP_201_CREATED)
    msg = 'Рецепта не существует или уже удален из избранного'
    return Response(msg, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'POST'])
@login_required
def api_shop_cart(request, id):
    user = request.user
    if Shop_card.objects.filter(user_id=user.id,
                                recipe_id=id).exists():
        if request.method == 'DELETE':
            Shop_card.objects.filter(user_id=user.id, recipe_id=id).delete()
            msg = 'Рецепт удален из списка покупок!'
            return Response(msg, status=status.HTTP_204_NO_CONTENT)
        if request.method == 'POST':
            msg = 'Уже есть в вашем списке покупок!'
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        if Shop_card.objects.create(user_id=user.id, recipe_id=id):
            msg = 'Рецепт добавлен в список!'
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
    msg = 'Рецепта не существует! Либо нет в вашем списке!'
    return Response(msg, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required
def load_shop_cart(request):
    shop_list = {}
    ingredients = IngredientsRecipe.objects.filter(
        recipe__shop_recipe__user=request.user
    )
    for object in ingredients:
        amount = object.amount
        name = get_object_or_404(Ingridient, id=object.id).name
        measurement_unit = get_object_or_404(Ingridient,
                                             id=object.id).measurement_unit
        if name not in shop_list:
            shop_list[name] = {
                'measurement_unit': measurement_unit,
                'amount': amount
            }
        else:
            shop_list[name]['amount'] += object.amount
    final_list = ([f'{key} - {value["amount"]} '
                  f'{value["measurement_unit"]} \n'
                   for key, value in shop_list.items()])
    response = HttpResponse(final_list, 'Content-Type: text/plain')
    response['Content-Disposition'] = 'attachment; filename="shop.txt"'
    return response
