from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.login_view, name='login'),
    path('index/', views.index_view, name='index'),
    path('teste/', views.teste_view, name='teste  '),
    
]