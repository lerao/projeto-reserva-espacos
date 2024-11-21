from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Servidor, Horario, Espaco, Reserva, ReservarHorario
from .serializers import ServidorSerializer, HorarioSerializer, EspacoSerializer, ReservaSerializer, ReservarHorarioSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import ReservaForm
from django.http import JsonResponse


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


from django.shortcuts import render
from .models import Espaco, Reserva, ReservarHorario

def index_view(request):
    espacos = Espaco.objects.all()
    reservas_por_espaco = {}

    for espaco in espacos:
        reservas = Reserva.objects.filter(espaco=espaco).order_by('data')
        reservas_detalhadas = []
        for reserva in reservas:
            horarios = ReservarHorario.objects.filter(reserva=reserva).select_related('numero_aula')
            reservas_detalhadas.append({
                'reserva': reserva,
                'horarios': horarios
            })
        reservas_por_espaco[espaco] = reservas_detalhadas

    context = {
        'espacos': espacos,
        'reservas_por_espaco': reservas_por_espaco,
    }
    return render(request, 'index.html', context)





@login_required
def logado_view(request):
    return render(request, 'index.html')

@login_required
def historico_reservas_view(request):
    return render(request, 'reserva/minhas_reservas.html')

@login_required
def espaco_view(request):
    
    return render(request, 'reserva/espaco.html', )

def horarios_disponiveis(request):
    print("Recebendo requisição AJAX")
    data = request.GET.get('data')
    espaco_id = request.GET.get('espaco')

    if not data or not espaco_id:
        print("Erro: Data ou espaço não fornecido")
        return JsonResponse({'error': 'Data ou espaço não fornecido.'}, status=400)

    try:
        horarios_ocupados = ReservarHorario.objects.filter(
            reserva__data=data,
            reserva__espaco_id=espaco_id
        ).values_list('numero_aula_id', flat=True)
        horarios_disponiveis = Horario.objects.exclude(id__in=horarios_ocupados).values('id', 'numero_aula', 'horario')
        print(f"Horários disponíveis: {list(horarios_disponiveis)}")
        return JsonResponse({'horarios': list(horarios_disponiveis)})
    except Exception as e:
        print(f"Erro ao processar: {str(e)}")
        return JsonResponse({'error': 'Erro ao processar a solicitação.'}, status=500)


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Espaco, Horario, Reserva, ReservarHorario

def criar_reserva(request):
    if request.method == 'POST':
        espaco_id = request.POST.get('espaco')
        data = request.POST.get('data')
        horarios_selecionados = request.POST.getlist('horarios')
        motivo = request.POST.get('motivo')
        turma = request.POST.get('turma')

        try:
            espaco = Espaco.objects.get(id=espaco_id)
        except Espaco.DoesNotExist:
            messages.error(request, "Espaço selecionado não existe.")
            return redirect('criar_reserva')

        # Validar horários
        horarios_disponiveis = []
        horarios_indisponiveis = []
        for horario_id in horarios_selecionados:
            try:
                horario = Horario.objects.get(id=horario_id)
                if ReservarHorario.objects.filter(
                    reserva__espaco=espaco, reserva__data=data, numero_aula=horario
                ).exists():
                    horarios_indisponiveis.append(horario)
                else:
                    horarios_disponiveis.append(horario)
            except Horario.DoesNotExist:
                messages.error(request, f"Horário inválido: {horario_id}.")
                return redirect('criar_reserva')

        # Se houver horários indisponíveis, exiba mensagem e volte ao formulário
        if horarios_indisponiveis:
            horarios_msg = ", ".join(
                [f"Aula {h.numero_aula} - {h.horario}" for h in horarios_indisponiveis]
            )
            messages.error(
                request, f"Os seguintes horários não estão disponíveis: {horarios_msg}."
            )
            return redirect('criar_reserva')

        # Criar a reserva
        reserva = Reserva.objects.create(
            matricula=request.user,  # Certifique-se de que o usuário está autenticado
            espaco=espaco,
            data=data,
            motivo=motivo,
            turma=turma,
        )

        for horario in horarios_disponiveis:
            ReservarHorario.objects.create(reserva=reserva, numero_aula=horario)

        messages.success(request, "Reserva criada com sucesso!")
        return redirect('index')

    # Renderizar formulário no caso de GET
    horarios = Horario.objects.all()
    espacos = Espaco.objects.filter(ativo=True)
    return render(request, 'reserva_form.html', {'horarios': horarios, 'espacos': espacos})
