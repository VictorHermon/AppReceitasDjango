from django.shortcuts import render
from receitas.models import Receita


def busca(request):
    """
    Busca as receitas que contem o nome informado
    :param request: Any
    :return: HttpResponse
    """
    lista_receita = Receita.objects.filter(publicado=True).order_by('-data_receita')

    receita_a_buscar = request.GET['buscar']
    lista_receitas = {
        'receitas': lista_receita.filter(nome_receita__icontains=receita_a_buscar)
    }

    return render(request, 'receitas/buscar.html', lista_receitas)
