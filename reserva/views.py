from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Servidor, Horario, Espaco, Reserva, ReservarHorario
from .serializers import ServidorSerializer, HorarioSerializer, EspacoSerializer, ReservaSerializer, ReservarHorarioSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


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
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        senha = request.POST.get('password')
        
        user = authenticate(request, matricula=matricula, password=senha)

        if user is not None:
            login(request, user)  # Realiza o login e salva na sessão
            return redirect('index')  # Redireciona para a página inicial
        else:
            messages.error(request, 'Matrícula ou senha inválidos.')

    return render(request, 'login.html')

def index_view(request):
    return render(request, 'index.html')

@login_required
def logado_view(request):
    return render(request, 'index.html')

@login_required
def historico_reservas_view(request):
    return render(request, 'reserva/minhas_reservas.html')

@login_required
def espaco_view(request):
    
    return render(request, 'reserva/espaco.html', )