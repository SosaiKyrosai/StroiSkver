from django.shortcuts import render, get_object_or_404, redirect
from home.models import paper
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



def edit_paper(request, paper_id):
    paper_obj = get_object_or_404(paper, id=paper_id)

    if request.method == 'POST':
        paper_obj.title = request.POST['title']
        paper_obj.textOfPaper = request.POST['textOfPaper']
        picture = request.FILES.get('pictureOfPaper')
        if picture:
            paper_obj.pictureOfPaper = picture
        paper_obj.save()
        return redirect('paper_list')  # Перенаправляем на страницу со списком статей

    # Если это GET-запрос, просто отображаем шаблон с данными статьи
    context = {'paper': paper_obj}
    return render(request, 'dashboard/edit_paper.html', context)


def paper_list(request):
    papers = paper.objects.all()
    context = {'papers': papers}
    return render(request, 'dashboard/paper_list.html', context)


@login_required
def user_admin(request):
    current_user = request.user

    # Получаем список всех пользователей, кроме текущего администратора
    users = User.objects.exclude(username=current_user.username)

    context = {
        'users': users,
    }

    return render(request, 'dashboard/user_admin.html', context)


@login_required
def make_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_superuser = True
    user.save()
    return redirect('user_admin')


@login_required
def remove_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_superuser = False
    user.save()
    return redirect('user_admin')