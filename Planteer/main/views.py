from django.shortcuts import render
from plants.models import Plant  # نموذج النباتات

def home_view(request):
    latest_plants = Plant.objects.filter(is_published=True)[:3]  # آخر 6 نباتات منشورة
    context = {
        'latest_plants': latest_plants,
        'page_title': 'Home'
    }
    return render(request, 'main/home.html', context)
