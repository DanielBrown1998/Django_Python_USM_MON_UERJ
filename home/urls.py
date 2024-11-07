from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [

    #uso livre.
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),

    path('monitorias/', views.monitoria, name='monitorias'),
    path('monitorias/search/', views.search_monitoria, name='search'),
    path('monitorias/update/<int:id>/', views.update_monitoria, name='update_monitoria'),

    #o usuário pode acessar.
    path('update/', views.update, name='update'),
    path('update/password/', views.password, name='password'),
    path('marcar_monitoria/', views.marcar_monitoria, name='marcar_monitoria'),

    #somente o super-user pode acessá-lo.
    path('data/', views.dados, name='dados'),
    path('config/', views.config, name='config'),
    path('config/search/', views.search_config, name='search_config'),
    path('config/update-monitoria/', views.update_monitorias, name='update_monitorias'),
    path('config/update-days/', views.update_days, name='update_days'),
    path('config/update-hours/', views.update_hours, name='update_hours'),
    path('config/matricula/', views.matricula, name='matricula'),
    path('config/matricula/create', views.create, name='create'),
    path('config/matricula/update', views.update_matricula, name='update_matricula'),
    path('config/matricula/delete', views.delete_matricula, name='delete_matricula'),
    path('config/usuarios', views.usuarios, name='usuarios'),
    path('config/usuarios/search', views.search_usuarios, name='search_usuarios'),    
    path('config/usuarios/update', views.update_usuarios, name='update_usuarios'),
]


#TODO: 
# 1 - disponibilizar o delete da conta do próprio usuário.


# # 2 - Montar view para expor ao usuário os dias que a monitoria pode ser marcada.
# OK 5 - inserir o filtro de dados datetime.now para o search_monitorias
# OK 6 - retirar o aside para o admin
# OK 8 - disponibilizar para o usuário somente os dias da semana que ele possui marcação de horario na tabela monitoria;
# OK 9 - requerer login para a view monitoria
# OK 10 - admin não pode marcar monitoria, alterar o aside, mostrar todas as monitoria marcadas para hoje no aside  


# OK 3 - atualizar o model de DataUser: inserir o atributo monitorias_ausentes
# 11 - add telefone ao campo de updates
# 12 - add telefone ao campo de cadastro

# OK 13 - add status ao models Monitorias
# OK 14 - add alteração de status para as monitorias do dia e antepassadas
# 15 - vincular os campos de datauser ao models monitoria
# 16 - alterar a view update_monitorias para realizar o TODO n° 14
# 7 - inserir regra de negócio: mais de 3 moonitorias ausentes sem aviso prévio, o usuario será suspenso do sistema
# 17 - Refatorar o cadastro
# 18 - Inserir o campo de recuperar senha
# 19 - add hora ao marcar monitoria