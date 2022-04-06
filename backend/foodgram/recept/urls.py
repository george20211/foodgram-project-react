from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('tags/', views.tags_get),
    path('tags/<int:id>/', views.tags_get_one),
    path('recipes/', views.Recipe_get.as_view()),
    path('recipes/<int:id>/', views.Recipe_one.as_view()),
    path('recipes/<id>/favorite/', views.favorite_post),
    path('recipes/<id>/shopping_cart/', views.api_shop_cart),
    path('recipes/download_shopping_cart/', views.load_shop_cart),
]
