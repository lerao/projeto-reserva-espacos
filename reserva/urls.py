from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', views.login_view, name='login'),
    path('logado/', views.logado_view, name='logado'),
    path('', views.index_view, name='index'),
    path('espaco/', views.espaco_view, name='espaco'),
    path('reserva/', views.criar_reserva, name='criar_reserva'),
    path('horarios-disponiveis/', views.horarios_disponiveis, name='horarios_disponiveis'),
    path('minhas-reservas/', views.minhas_reservas_view, name= 'minhas_reservas'),
    path('cancelar-reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
]
