from home.views import message
from home.forms.update_create_form import UpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url="home:home")
def update(request):
    
    if request.method == 'POST':
        form = UpdateForm(data=request.POST, instance=request.user)
        context = {
        'title': 'Update',
        'form': form,
        }
        if form.is_valid():     
            form.save()
            message(request, 'Atualizado com sucesso', sucesss=True)
            return redirect('home:home')

        else:
            message(request, 'Erro ao atualizar', error=True)
            url = 'home/update.html'
            return render(request, url, context=context)

    form = UpdateForm(instance=request.user)
    context = {
        'title': 'Update',
        'form': form,
    }
    url = 'home/update.html'
    return render(request, url, context=context)
