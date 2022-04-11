from django.shortcuts import render
from receitas.models import Receita
from django.core.paginator import Paginator


def index(request):
    """
    Mostra as receitas que foram publicadas pelos usuarios
    :param request: Any
    :return: HttpResponse
    """
    receitas = Receita.objects.filter(publicado=True).order_by('-data_receita')
    paginator = Paginator(receitas, 3)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)

    receitas = {
        'receitas': receitas_por_pagina
    }
    return render(request, 'receitas/index.html', receitas)
