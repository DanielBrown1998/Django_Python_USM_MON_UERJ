from django.shortcuts import render, redirect
from home.models import Matriculas
from django.contrib.auth.decorators import login_required
from home.views import message

@login_required(login_url="home:index")
def matricula(request):
    from home.models import Matriculas
    matriculas = Matriculas.objects.all()
    context = {
        'title': 'Matriculas',
        'matriculas': matriculas,
    }

    url = 'home/matricula.html'
    return render(request, url, context=context)

@login_required(login_url="home:index")
def create(request):
    context = {
        'title': 'Criando Matricula',
        }
    matricula = request.POST.get('matricula', '').strip()
    if matricula:
        matricula = Matriculas(
            matricula=matricula
        )
        matricula.save()
        message(request, 'Matricula Salva com Sucesso', sucesss=True)
    return redirect('home:matricula')

@login_required(login_url="home:index")
def update_matricula(request):
    context = {
        'title': 'atualizando Matricula',
        }
    
    matricula_antiga_id = request.POST.get('matricula_antiga_id', '').strip()
    matricula_nova = request.POST.get('matricula_nova', '').strip()
    if matricula_nova:
        print(matricula_nova)
    if matricula_antiga_id:
        print(matricula_antiga_id)
    return redirect('home:matricula')

@login_required(login_url="home:index")
def delete_matricula(request):
    
    matricula = request.POST.get('matricula', '').strip()
    
    delete_all = request.POST.get('delete_all', '').strip()
    
    confirmation = request.POST.get('confirmation', 'no').strip()
    
    matriculas = []
    if delete_all:
        matriculas = Matriculas.objects.all()
        
    if matricula:
        print(matricula)
    
    if confirmation != 'no':
        if matriculas:
            matriculas.delete()
        return redirect('home:matricula')

    context = {
        'title': 'Deletando Matricula',
        'confirmation': confirmation,
        'delete_all': delete_all,
        'matricula': matricula,
        'matriculas': matriculas,
    }

    return render(
        request, 'home/matricula.html', context=context
    )