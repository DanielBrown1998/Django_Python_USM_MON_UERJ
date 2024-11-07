from home.forms.update_create_form import UpdatePassword
from home.views import message
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import auth
@login_required(login_url="home:home")
def password(request):

    if request.method == 'POST':
        form = UpdatePassword(data=request.POST, instance=request.user)
        context = {
            'title': 'Update Password',
            'form': form,
        }
        if form.is_valid():
            form.save()
            auth.logout(
                request
            )
            message(request, 'Senha alterada!!!', sucesss=True)
        else:
            message(request, 'Erro ao alterar a senha!!!', error=True)
            url = 'home/update.html'
            return render(request, url, context=context)
        url = 'home/index.html'
        return render(request, url, context=context)

    form = UpdatePassword(instance=request.user)
    context = {
        'title': 'Update Password',
        'form': form,
    }
    url = 'home/password.html'
    return render(request, url, context=context)