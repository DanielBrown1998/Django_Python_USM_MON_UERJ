from django.shortcuts import render, redirect
from home.forms.update_create_form import CreateForm
from home.views import message
from home.models import DataUser, Matriculas
def cadastro(request):

    if request.method == 'POST':
        form = CreateForm(
            request.POST
        )
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            data_user = DataUser(owner=user)
            data_user.save()
            matricula = Matriculas.objects.get(
                matricula=form.cleaned_data['username']
            )
            matricula.status = True
            matricula.save()

            form.save()
            message(request, 'Cadastro realizado com sucesso!', sucesss=True)
            return redirect('home:home')
        message(request, 'Atente-se aos requisitos!!!')
        context = {
        'title': 'Cadastro',
        'form': form,
        }
        url = 'home/cadastro.html'
        return render(request, url, context=context)