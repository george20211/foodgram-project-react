from django.urls import path
from . import views
from .views import UserViewSet

app_name = 'users'

urlpatterns = [
    path('subscriptions',  views.Subs.as_view()),
    path('<id>/', UserViewSet),
    path('<id>/subscribe/', views.api_posts),
]
