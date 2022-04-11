from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita


def cadastro(request):
    """
    Cadastra uma nova pessoa no sistema
    :param request: Any
    :return: HttpResponse
    """
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        if campo_vazio(nome):
            messages.error(request, 'Nome invalido')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'E-mail invalido')
            return redirect('cadastro')
        if senha_nao_sao_iguais(senha, senha2):
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')
        if email_ja_existe(email) or nome_ja_existe(nome):
            return messages.error(request, 'Esse usuario já está cadastrado')

        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Cadastrado realizado com sucesso')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    """
    Realiza o login de uma pessoa no sistema
    :param request: Any
    :return: HttpResponse
    """
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        if campo_vazio(email):
            messages.error(request, 'Valor invalido no campo email')
            return redirect('login')
        if campo_vazio(senha):
            messages.error(request, 'Valor invalido no campo senha')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user:
                auth.login(request, user)
                print('Login realizado com sucesso')
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')


def logout(request):
    """
    Realiza o logout do usuario no sistema
    :param request: Any
    :return: HttpResponse
    """
    auth.logout(request)
    return redirect('index')


def dashboard(request):
    """
    Mostra as receitas publicadas no sistema pelos usuarios
    :param request: Any
    :return: HttpResponse
    """
    if request.user.is_authenticated:
        dados = {
            'receitas': Receita.objects.filter(pessoa=request.user.id).order_by('-data_receita')
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


def campo_vazio(campo):
    """
    Verificar se o campo informado está em branco ou vazio
    :param campo: String
    :return: Bool
    """
    return not campo.strip()


def senha_nao_sao_iguais(senha, senha2):
    """
    Verifica se as senhas informadas são iguais
    :param senha: String
    :param senha2: String
    :return: Bool
    """
    return senha != senha2


def email_ja_existe(email):
    """
    Verifica se o email informado já existe no banco
    :param email: String
    :return: Bool
    """
    return User.objects.filter(email=email).exists()


def nome_ja_existe(nome):
    """
    Verifica se o nome informado já existe no banco
    :param nome: String
    :return: Bool
    """
    return User.objects.filter(username=nome).exists()
