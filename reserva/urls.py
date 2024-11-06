from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'servidores', views.ServidorViewSet)
router.register(r'horarios', views.HorarioViewSet)
router.register(r'espacos', views.EspacoViewSet)
router.register(r'reservas', views.ReservaViewSet)
router.register(r'reserva_horarios', views.ReservaHorarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login_view, name='login'),

    
]