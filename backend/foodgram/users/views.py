from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.decorators import login_required
from .models import User, Follow
from .serializers import FollowListSerializer, IamSerializer
from django.http import JsonResponse


@api_view(['GET'])
def i_am_get(request):
    user = get_object_or_404(User, id=request.user.id)
    serializer = IamSerializer(user)
    return JsonResponse(serializer.data)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()

    @action(detail=False, url_path='me')
    def me(request, id):
        msg = 'OK'
        return Response(msg, status=status.HTTP_200_OK)


@api_view(['DELETE', 'POST'])
@login_required
def api_posts(request, id):
    author = get_object_or_404(User, id=id)
    user = request.user
    if request.method == 'POST':
        if author != user:
            if Follow.objects.filter(author=author, user=user).exists():
                msg = 'Уже есть'
                return Response(msg, status=status.HTTP_204_NO_CONTENT)
            msg = 'OK'
            Follow.objects.create(author=author, user=user)
            return Response(msg, status=status.HTTP_200_OK)
        msg = 'На себя нельзя подписаться'
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        if Follow.objects.filter(author=author, user=user).exists():
            Follow.objects.filter(author=author, user=user).delete()
            msg = 'Вы отписались!'
            return Response(msg, status=status.HTTP_204_NO_CONTENT)
        msg = 'Вы не подписаны на пользователя'
        return Response(msg, status=status.HTTP_404_NOT_FOUND)


class Subs(generics.ListAPIView):
    def get(self, request):
        obj = Follow.objects.filter(user_id=request.user.id)
        pages = self.paginate_queryset(obj)
        serializer_class = FollowListSerializer(
            instance=pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer_class.data)


class Users_all(generics.ListAPIView):
    def get(self, request):
        obj = User.objects.all()
        pages = self.paginate_queryset(obj)
        serializer_class = IamSerializer(
            instance=pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer_class.data)
