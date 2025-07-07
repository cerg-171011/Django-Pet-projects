from django.shortcuts import render, redirect, get_object_or_404
from .models import Diary, Comment, Like
from .forms import CommentForm, DiaryForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_list')
    else:
        if request.user.is_authenticated:
            return redirect('main_list')
        form = AuthenticationForm()
    return render(request, 'appcomment/login.html', {"form": form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.user = request.user
            user.save()
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('main_list')
        form = UserCreationForm()
    return render(request, 'appcomment/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def main_list_view(request):
    if request.method == 'POST':
        if request.POST.get('form-type') == 'diary':
            diary_form = DiaryForm(request.POST)
            comment_form = CommentForm()
            if diary_form.is_valid():
                entry = diary_form.save(commit = False)
                entry.user = request.user
                entry.save()
                return redirect('main_list')
        elif request.POST.get('form-type') == 'comment':
            comment_form = CommentForm(request.POST)
            diary_form = DiaryForm()
            if comment_form.is_valid():
                comment = comment_form.save(commit = False)
                comment.user = request.user
                comment.save()
                return redirect('main_list')
    else:
        diary_form = DiaryForm()
        comment_form = CommentForm()
        
        diary_app = Diary.objects.all().order_by('-created_at')
        comments_app = Comment.objects.all().order_by('-created_at')
        
    return render(request, 'appcomment/main_list.html', {'diary_form': diary_form, 'comment_form': comment_form, 'diary_app': diary_app, 'comment_app': comments_app})
    
    
def delete_view(request, id_entry):
    entry = get_object_or_404(Diary, id = id_entry)
    print(entry)
    entry.delete()
    return redirect('main_list')

def update_view(request, id_entry):
    entry = get_object_or_404(Diary, id = id_entry)
    if request.method == 'POST':
        diary_form = DiaryForm(request.POST, instance = entry)
        comment_form = CommentForm()
        if diary_form.is_valid():
            diary_form.save()
            return redirect('main_list')
    else:
        diary_form = DiaryForm(instance = entry)
        comment_form = CommentForm()
    diary_app = Diary.objects.all().order_by('-created_at')
    comment_app = Comment.objects.all().order_by('-created_at')
    return render(request, 'appcomment/main_list.html', {'diary_form'
    '': diary_form, 'comment_form': comment_form, 'diary_app': diary_app, 'comment_app': comment_app})


def add_comment(request, id_entry):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit = False)
            comment.user = request.user
            diary = Diary.objects.get(id = id_entry)
            comment.diary_entry = diary
            comment.save()
            print('Сохранили комментарий:', comment.text)
            return redirect('main_list')
    else:
        comment_form = CommentForm()
    comment_app = Comment.objects.all().order_by('-created_at')
    diary_app = Diary.objects.all().order_by('-created_at')
    diary_form = DiaryForm()
    return render(request, 'appcomment/main_list.html', {'diary_form'
    '': diary_form, 'comment_form': comment_form, 'diary_app': diary_app, 'comment_app': comment_app})



def like_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        comment_id = data.get('comment_id')
        comment = Comment.objects.get(id=comment_id)

        like, created = Like.objects.get_or_create(user=request.user, comment=comment)

        if not created:
            like.delete()
        
        return JsonResponse({
            'likes_count': Like.objects.filter(comment=comment).count()
        })