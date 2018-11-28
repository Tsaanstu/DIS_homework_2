from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginator(user_list, request):
    paginator = Paginator(user_list, 10)

    page = request.GET.get('page')
    try:
        user_list = paginator.page(page)
    except PageNotAnInteger:
        user_list = paginator.page(1)
    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)
    return user_list


def index(request):
    user_list = [
        {"name": "Ivanov Ivan Number1", "id": 1},
        {"name": "Ivanov Ivan Number2", "id": 2},
        {"name": "Ivanov Ivan Number3", "id": 3},
        {"name": "Ivanov Ivan Number4", "id": 4},
        {"name": "Ivanov Ivan Number5", "id": 5},
        {"name": "Ivanov Ivan Number6", "id": 6},
        {"name": "Ivanov Ivan Number7", "id": 7},
        {"name": "Ivanov Ivan Number8", "id": 8},
        {"name": "Ivanov Ivan Number9", "id": 9},
        {"name": "Ivanov Ivan Number10", "id": 10},
        {"name": "Ivanov Ivan Number11", "id": 11},
        {"name": "Ivanov Ivan Number12", "id": 12},
        {"name": "Ivanov Ivan Number13", "id": 13},
        {"name": "Ivanov Ivan Number14", "id": 14},
        {"name": "Ivanov Ivan Number15", "id": 15},
        {"name": "Ivanov Ivan Number16", "id": 16},
        {"name": "Ivanov Ivan Number17", "id": 17},
        {"name": "Ivanov Ivan Number18", "id": 18},
        {"name": "Ivanov Ivan Number19", "id": 19},
        {"name": "Ivanov Ivan Number20", "id": 20},
    ]
    user_list = paginator(user_list, request)
    return render(request, 'bs/index.html', {"users": user_list})


def login(request):
    return render(request, 'bs/login.html', {})
