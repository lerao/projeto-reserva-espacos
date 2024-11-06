from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Servidor, Horario, Espaco, Reserva, ReservarHorario
from .serializers import ServidorSerializer, HorarioSerializer, EspacoSerializer, ReservaSerializer, ReservarHorarioSerializer


# Create your views here.

class ServidorViewSet(viewsets.ModelViewSet):
    queryset = Servidor.objects.all()
    serializer_class = ServidorSerializer

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer

class EspacoViewSet(viewsets.ModelViewSet):
    queryset = Espaco.objects.all()
    serializer_class = EspacoSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

class ReservaHorarioViewSet(viewsets.ModelViewSet):
    queryset = ReservarHorario.objects.all()
    serializer_class = ReservarHorarioSerializer



def login_view(request):
    return render(request, 'login.html')

@login_required
def solicitacao_reserva_view(request):
    return render(request, 'reserva/solicitacao_reserva.html')

@login_required
def historico_reservas_view(request):
    return render(request, 'reserva/minhas_reservas.html')