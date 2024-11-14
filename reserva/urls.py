from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', views.login_view, name='login'),
    path('logado/', views.logado_view, name='logado'),
    path('', views.index_view, name='index'),
    
]