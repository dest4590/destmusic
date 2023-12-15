from django.shortcuts import render, HttpResponse, redirect
from .models import Music, Author, Update
from Core.settings import DEVELOPMENT
from django.http import JsonResponse
from collections import Counter
import json


def is_admin(user):
    return user.is_superuser

if DEVELOPMENT:
    def index(request):
        return HttpResponse('development mode enabled, please wait until author it off')

    def index_development(request):
        return render(
            request,
            'index.html',
            {'songs': Music.objects.all(), 'authors_count': len(Author.objects.all())},
        )

else:
    def index(request):
        return render(
            request,
            'index.html',
            {
                'songs': Music.objects.all(),
                'authors_count': len(Author.objects.all()),
                'is_admin': True if request.user.is_superuser else False,
                'genres': [genre for genre, count in Counter(Music.objects.values_list('genre', flat=True)).items() if count >= 2]
            },
        )


def updates(request):
    return render(request, 'updates.html', {'updates': Update.objects.order_by('-id'), 'all': True})

def update(request, version: str):
    try:
        return render(request, 'updates.html', {'update': Update.objects.get(version=version), 'all': False})
    except Update.DoesNotExist:
        return render(request, 'updates.html', {'not_found': True})

def author(request, name: str):
    try:
        author = Author.objects.get(name__startswith=name.lower())
        songs = Music.objects.filter(author__startswith=name.lower())

        return render(request, 'author.html', {'author': author, 'songs': songs})

    except Author.DoesNotExist:
        return render(request, 'author.html', {'error': True})

def upload(request):
    return HttpResponse('<h1>Uploads<h1>')


def dash(request):
    return redirect('https://dash.cloudflare.com/')