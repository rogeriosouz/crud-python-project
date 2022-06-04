from time import sleep
from PySimpleGUI import PySimpleGUI as sg
from decouple import config
import pymongo

NAME_BASEDB = config('NAME_BASEDB')
client = pymongo.MongoClient(NAME_BASEDB)
base_de_dados = client['sistem_de_usuario_alunos_tela']
bd_usuario = base_de_dados.get_collection('usuarios')
bd_alunos = base_de_dados.get_collection('alunos')

sg.theme('DarkAmber')


def interface_01():
    leyout = [
        [sg.Text('SISTEMA DE ALUNOS COM TELA')],
        [sg.Text('Login_cadastro')],
        [sg.Button('login', size=(20, 0))],
        [sg.Button('Cadastrar', size=(20, 0))],
    ]

    janela_inicio = sg.Window(
        'inicio', leyout, finalize=True, element_justification='center')

    # eventos janela_inicio
    eventos, valores = janela_inicio.read()
    return janela_inicio, eventos


janela_inicio, eventos = interface_01()


def esister_email_bd(email):
    bd = bd_usuario.find({
        "email": email,
    })

    email = ''

    for x in bd:
        email = x['email']

    if email == '':
        return False
    else:
        return True


def esister_senha_bd(senha):
    bd = bd_usuario.find({
        "senha": senha,
    })

    email = ''

    for x in bd:
        email = x['senha']

    if email == '':
        return False
    else:
        return True


def esister_nome_alunos_bd(nome):
    bd = bd_alunos.find({
        "nome": nome,
    })

    nome = ''

    for x in bd:
        nome = x['nome']

    if nome == '':
        return False
    else:
        return True


def pegar_nome(email):
    bd = bd_usuario.find({
        "email": email,
    })

    for x in bd:
        nome = x['nome']

    return nome


def verificar_alunos_bd(nome, idade, turma):
    bd = bd_alunos.find({
        "nome": nome,
        "idade": idade,
        "turma": turma
    })

    nome = ''
    idade = ''
    turma = ''

    for x in bd:
        nome = x['nome']
        idade = x['idade']
        turma = x['turma']

    if nome == '' and idade == '' and turma == '':
        return False
    else:
        return True

# cadastra alunos


def cadastra_alunos():
    layout_cadastra_aluno = [
        [sg.Text('Cadastrar Aluno', size=(30, 0))],
        [sg.Text('Nome Completo:'), sg.Input(key='nome', size=(30, 0))],
        [sg.Text('Idade:  '), sg.Input(key='idade', size=(15, 0))],
        [sg.Text('Turma: '), sg.Input(key='turma', size=(15, 0))],
        [sg.Button('cadastra')],
        [sg.Text(key='error-cadastro', text_color='red')],
    ]

    janela_de_cadastro = sg.Window(
        'cadastro_aluno', layout=layout_cadastra_aluno, finalize=True,
        element_justification='left')
    while True:
        eventos, valores = janela_de_cadastro.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        elif eventos == 'cadastra':
            if verificar_alunos_bd(valores['nome'], valores['idade'],
                                   valores['turma']):
                janela_de_cadastro['error-cadastro'].update(
                    'erro aluno ja esistente')

            else:
                if valores['nome'] == '' or valores[
                    'idade'] == '' or valores[
                        'turma'] == '':
                    janela_de_cadastro['error-cadastro'].update(
                        'erro campo vazio')
                else:
                    bd_alunos.insert_one({
                        "nome": valores['nome'],
                        "idade": valores['idade'],
                        "turma": valores['turma']
                    })
                    janela_de_cadastro.close()
                    sleep(1)
                    pag_principal()

# amostra alunos


def read_alunos():
    layout_ler_alunos = [
        [sg.Text('nome'), sg.Text('idade'), sg.Text('Turma')],
    ]

    janela_read_alunos = sg.Window(
        'ler_alunos', layout_ler_alunos, element_justification='left')

    for bd in bd_alunos.find():
        lista_row = [
            [sg.Text(bd['nome']),
             sg.Text(bd['idade']),
                sg.Text(bd['turma'])],
        ]
        janela_read_alunos.add_rows(lista_row)
    lina_butao = [
        [sg.Button('voltar', size=(20, 0))],
    ]

    janela_read_alunos.add_row(lina_butao)
    janela_read_alunos.BackgroundColor = '#808080'
    while True:
        eventos, valores = janela_read_alunos.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        elif eventos == 'voltar':
            janela_read_alunos.close()
            sleep(1)
            pag_principal()

# editar aluno bd


def editar_aluno_bd(nome_antigo, nome_novo, idade_novo, turma_novo):
    bd_aluno = bd_alunos.find({
        'nome': nome_antigo
    })

    for bd in bd_aluno:
        nome_antigo = bd['nome']
        idade_antigo = bd['idade']
        turma_antigo = bd['turma']

    alunos = {
        "nome": nome_antigo,
        "idade": idade_antigo,
        "turma": turma_antigo
    }

    alunos_novo = {
        "$set": {
            "nome": nome_novo,
            "idade": idade_novo,
            "turma": turma_novo
        }
    }

    bd_alunos.update_one(alunos, alunos_novo)

# editar aluno


def editar_alunos():
    layout_editar = [
        [sg.Text('Editar aluno', size=(30, 0))],
        [sg.Text(key='nome_aluno')],
        [sg.Text('Nome Completo:'), sg.Input(key='nome', size=(30, 0))],
        [sg.Text('Idade:  '), sg.Input(key='idade', size=(15, 0))],
        [sg.Text('Turma: '), sg.Input(key='turma', size=(15, 0))],
        [sg.Button('editar')],
        [sg.Text(key='error-cadastro', text_color='red')],
    ]

    layout_nome_editar = [
        [sg.Text('Digite o nome completo do aluno que voçe que editar')],
        [sg.Text('Nome: '), sg.Input(key='nome', size=(40, 0))],
        [sg.Text(key='error_nome', text_color='red')],
        [sg.Button('Enviar')],
    ]

    janela_nome_editar = sg.Window('editar_nome', layout=layout_nome_editar,
                                   finalize=True,
                                   element_justification='left')

    while True:
        eventos, valores_nome_edit = janela_nome_editar.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        if eventos == 'Enviar':
            if esister_nome_alunos_bd(valores_nome_edit['nome']):
                janela_editar = sg.Window('editar', layout_editar,
                                          element_justification='left',
                                          finalize=True)
                janela_editar['nome_aluno'].update(
                    valores_nome_edit['nome'])

                while True:
                    eventos, valores = janela_editar.read()
                    if eventos == sg.WINDOW_CLOSED:
                        break
                    elif eventos == 'editar':
                        nome_novo = valores['nome']
                        idade_novo = valores['idade']
                        turma_novo = valores['turma']

                        nome_antigo = valores_nome_edit['nome']
                        editar_aluno_bd(nome_antigo, nome_novo,
                                        idade_novo, turma_novo)
                        janela_editar.close()
                        sleep(1)
                        pag_principal()
                        break

            else:
                janela_nome_editar['error_nome'].update('Nome Nao foi'
                                                        ' encontrado, O nome'
                                                        ' tem ser o que foi'
                                                        ' cadastrado')

# excluir aluno


def excluir_aluno():
    layaut_escluir_aluno = [
        [sg.Text('EXCLUIR ALUNO')],
        [sg.Text('NOME ALUNO: '), sg.Input(key='nome')],
        [sg.Button('excluir')],
        [sg.Text(key='errro_excluir', text_color='red')],
    ]

    layaut_escluir_aluno_confirmar = [
        [sg.Text('Tem serteza')],
        [sg.Button('confirmar', size=(20, 0))],
        [sg.Button('cancelar', size=(20, 0))],
    ]

    janela_escluir_aluno = sg.Window(
        'escluir', layout=layaut_escluir_aluno,
        element_justification='left', finalize=True)

    while True:
        eventos_esxluir, valores = janela_escluir_aluno.read()
        if eventos_esxluir == sg.WINDOW_CLOSED:
            break
        elif eventos_esxluir == 'excluir':
            if esister_nome_alunos_bd(valores['nome']):
                janela_confimar_escluir = sg.Window(
                    'confirmar_excluir', layout=layaut_escluir_aluno_confirmar,
                    element_justification='center')
                while True:
                    eventos_confirmar, valo_c = janela_confimar_escluir.read()
                    if eventos_confirmar == sg.WINDOW_CLOSED:
                        break
                    elif eventos_confirmar == 'confirmar':
                        bd_alunos.delete_one({
                            'nome': valores['nome']
                        })
                        janela_confimar_escluir.close()
                        janela_escluir_aluno.close()
                        sleep(1)
                        pag_principal()
                    elif eventos_confirmar == 'cancelar':
                        janela_confimar_escluir.close()
                        janela_escluir_aluno.close()
                        sleep(1)
                        pag_principal()
            else:
                janela_escluir_aluno['errro_excluir'].update(
                    'Aluno não foi encontrado')

# editar usuario


def editar_usuario(email_antigo, senha_antiga):
    layout_edit = [
        [sg.Text('EDITAR USUARIO')],
        [sg.Text('email_novo: '), sg.Input(key='email_novo')],
        [sg.Text('senha_nova:'), sg.Input(key='senha_novo', size=(20, 0),
                                          password_char='*')],
        [sg.Button('editar')],
        [sg.Text(key='error_email', text_color='red')],
    ]

    janela_usuario_edit = sg.Window(
        'edit_usuario', layout=layout_edit, element_justification='left',
        finalize=True)
    while True:
        eventos, valores = janela_usuario_edit.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        if eventos == 'editar':
            email_novo = valores['email_novo']
            senha_nova = valores['senha_novo']

            if esister_email_bd(email_novo):
                janela_usuario_edit['error_email'].update('Email invalido!')
            else:
                usuario_antigo = {
                    'email': email_antigo,
                    'senha': senha_antiga,
                }

                usuario_novo = {
                    "$set": {
                        'email': email_novo,
                        'senha': senha_nova
                    }
                }

                bd_usuario.update_one(usuario_antigo, usuario_novo)
                janela_usuario_edit.close()
                pag_principal(email_novo, senha_nova)

#  pagina principal


def pag_principal(email='', senha=''):
    layout_cadastra_aluno = [
        [sg.Text('PROGRAMA DE ALUNOS COM TELA')],
        [sg.Button('Cadastra-alunos', size=(20, 0))],
        [sg.Button('Ver-alunos', size=(20, 0))],
        [sg.Button('Editar-aluno', size=(20, 0))],
        [sg.Button('Excluir-aluno', size=(20, 0))],
        [sg.Text('USUARIO')],
        [sg.Button('Editar-usuario', size=(20, 0))]
    ]

    janela_principal = sg.Window(
        'janela_principal', layout=layout_cadastra_aluno, finalize=True,
        element_justification='center')

    while True:
        eventos, valores = janela_principal.read()

        if eventos == sg.WINDOW_CLOSED:
            break
        elif eventos == 'Cadastra-alunos':
            janela_principal.close()
            sleep(1)
            cadastra_alunos()
            break
        elif eventos == 'Ver-alunos':
            janela_principal.close()
            sleep(1)
            read_alunos()
            break
        elif eventos == 'Editar-aluno':
            janela_principal.close()
            sleep(1)
            editar_alunos()
            break
        elif eventos == 'Excluir-aluno':
            janela_principal.close()
            sleep(1)
            excluir_aluno()
            break
        elif eventos == 'Editar-usuario':
            janela_principal.close()
            sleep(1)
            editar_usuario(email, senha)
            break

# fazer o login


def fazer_login(valores, janela_login):
    # ferificar se o email e a senha estao na bd
    # email
    janela_login['email_error'].update('')
    janela_login['senha_error'].update('')
    janela_login['logado'].update('')
    if not esister_email_bd(valores['email']):
        janela_login['email_error'].update('email invalido!')
    # senha
    if len(valores['senha']) < 5 or len(valores['senha']) > 50:
        janela_login['senha_error'].update(
            'senha pressisa ter de 5 a 50 caracteres!')

    if len(valores['senha']) < 5 or len(
            valores['senha']) > 50 and not esister_email_bd(
                valores['email']):
        janela_login['email_error'].update('email invalido!')
        janela_login['senha_error'].update(
            'senha pressisa ter de 5 a 50 caracteres!')

    if esister_email_bd(valores['email']) and esister_senha_bd(
            valores['senha']):
        janela_login['email_error'].update('')
        janela_login['senha_error'].update('')
        sleep(1)
        janela_login.close()
        sleep(1)
        pag_principal(valores['email'], valores['senha'])
    else:
        janela_login['logado'].update('Email ou senha invalidos!!')

# login usuario


def login():
    leyout_login = [
        [sg.Text('email: '), sg.Input(key='email')],
        [sg.Text(key='email_error', text_color='red')],
        [sg.Text('senha:'), sg.Input(key='senha', password_char='*')],
        [sg.Text(key='senha_error', text_color='red')],
        [sg.Button('Logar')],
        [sg.Text(key='logado', text_color='red')]
    ]

    janela_login = sg.Window('login', leyout_login, finalize=True)

    while True:
        eventos, valores = janela_login.read()

        if eventos == sg.WINDOW_CLOSED:
            break
        if eventos == 'Logar':
            fazer_login(valores, janela_login)

# cadastrar usuario na base de dados


def cadastrar_bd(valores, janela_cadastro):
    # verificar se ja esister na bd_dados o email
    janela_cadastro['error_email'].update('')
    janela_cadastro['error_senha'].update('')

    if esister_email_bd(valores['email']):
        janela_cadastro['error_email'].update('email ja esistente')
    # verificar se a senha tem de 5 a 50 caracteres
    elif len(valores['senha']) < 5 or len(valores['senha']) > 50:
        janela_cadastro['error_senha'].update(
            'senha pressisa ter de 5 a 50 caracteres')
    else:
        # se passa por isso cadastra na base de dados

        bd_usuario.insert_one({
            "email": valores['email'],
            "senha": valores['senha']
        })

        janela_cadastro['cadastro_su'].update('Cadastrado com susseso')
        sleep(1)
        janela_cadastro.close()
        sleep(1)

        pag_principal(valores['email'], valores['senha'])

# cadastrar usuario


def cadastrar():
    leyout_cadastro = [
        [sg.Text('email: '), sg.Input(key='email')],
        [sg.Text(key='error_email', size=(30, 0), text_color='red')],
        [sg.Text('senha:'), sg.Input(key='senha', password_char='*')],
        [sg.Text(key='error_senha', size=(30, 0), text_color='red')],
        [sg.Button('cadastrar')],
        [sg.Text(key='cadastro_su', text_color='green')]
    ]

    janela_cadastro = sg.Window(
        'tela_de_cadastro', leyout_cadastro, finalize=True)

    while True:
        eventos, valores = janela_cadastro.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        if eventos == 'cadastrar':
            cadastrar_bd(valores, janela_cadastro)


while True:
    if eventos == sg.WINDOW_CLOSED:
        break

    if eventos == 'login':
        janela_inicio.close()
        sleep(2)
        login()
        break

    if eventos == 'Cadastrar':
        janela_inicio.close()
        sleep(2)
        cadastrar()
        break
