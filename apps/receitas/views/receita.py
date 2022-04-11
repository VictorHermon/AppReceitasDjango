from django.shortcuts import render, get_object_or_404, redirect
from receitas.models import Receita
from django.contrib.auth.models import User


def receita(request, receita_id):
    """
    Exibe a receita informada caso exista no banco
    :param request: Any
    :param receita_id: int
    :return: HttpResponse
    """
    receita_exibir = {
        'receita': get_object_or_404(Receita, pk=receita_id)
    }
    return render(request, 'receitas/receita.html', receita_exibir)


def cria_receita(request):
    """
    Cria a receita no sistema conforme os dados informados
    :param request: Any
    :return: HttpResponse
    """
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes,
                                         modo_preparo=modo_preparo, tempo_preparo=tempo_preparo, rendimento=rendimento,
                                         categoria=categoria, foto_receita=foto_receita)
        receita.save()
        return redirect('dashboard')
    else:
        return render(request, 'receitas/cria_receita.html')


def deleta_receita(request, receita_id):
    """
    Deleta uma receita com base no id informado
    :param request: Any
    :param receita_id: int
    :return: HttpResponse
    """
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')


def edita_receita(request, receita_id):
    """
    Edita uma receita com base no id informado
    :param request: Any
    :param receita_id: int
    :return: HttpResponse
    """
    receita_a_editar = {
        'receita': get_object_or_404(Receita, pk=receita_id)
    }
    return render(request, 'receitas/edita_receita.html', receita_a_editar)


def atualiza_receita(request):
    """
    Atualiza os dados informados de uma receita no banco
    :param request: Any
    :return: HttpResponse
    """
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        receita = Receita.objects.get(pk=receita_id)
        receita.nome_receita = request.POST['nome_receita']
        receita.ingredientes = request.POST['ingredientes']
        receita.modo_preparo = request.POST['modo_preparo']
        receita.tempo_preparo = request.POST['tempo_preparo']
        receita.rendimento = request.POST['rendimento']
        receita.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            receita.foto_receita = request.FILES['foto_receita']
        receita.save()
        return redirect('dashboard')
