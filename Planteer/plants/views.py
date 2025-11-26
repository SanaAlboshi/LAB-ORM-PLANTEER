from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg
from .models import Plant, Review, Country, CATEGORY_CHOICES
from .forms import PlantForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from .forms import ReviewForm



def plants_list(request):
    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')
    country_id = request.GET.get('country')
    
    # تنظيف القيم - تحويل 'None' string إلى None
    if category == 'None' or category == '':
        category = None
    if is_edible == 'None' or is_edible == '':
        is_edible = None
    if country_id == 'None' or country_id == '':
        country_id = None

    plants = Plant.objects.filter(is_published=True)

    if category:
        plants = plants.filter(category=category)
    if is_edible in ['true','false']:
        plants = plants.filter(is_edible=(is_edible=='true'))
    if country_id:
        plants = plants.filter(countries__id=country_id)

    # إضافة Pagination
    paginator = Paginator(plants, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    countries = Country.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': CATEGORY_CHOICES,
        'category': category,
        'is_edible': is_edible,
        'countries': countries,
        'selected_country': country_id,
    }
    return render(request, 'plants/plants_list.html', context)

def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)

    # Related Plants
    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:4]

    # جلب التعليقات المرتبطة بالنبتة
    reviews = plant.reviews.all().order_by('-created_at')

    # إحصائيات الريتينق باستخدام aggregate
    stats = reviews.aggregate(
        total_reviews=Count('id'),
        avg_rating=Avg('rating')
    )

    # طباعة النتائج في التيرمنال
    print(f"Stats for {plant.name}: {stats}")

    context = {
        'plant': plant,
        'related_plants': related_plants,
        'reviews': reviews,
        'stats': stats,
    }
    return render(request, 'plants/plant_detail.html', context)



@staff_member_required
def plant_create(request):
    form = PlantForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('plants_list')
    return render(request, 'plants/plant_form.html', {'form': form})



@staff_member_required
def plant_update(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    form = PlantForm(request.POST or None, request.FILES or None, instance=plant)
    if form.is_valid():
        form.save()
        return redirect('plant_detail', pk=plant.pk)
    return render(request, 'plants/plant_form.html', {'form': form})


@staff_member_required
def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == 'POST':
        plant.delete()
        return redirect('plants_list')
    return render(request, 'plants/plant_delete.html', {'plant': plant})

def plant_search(request):
    query = request.GET.get('q')
    results = Plant.objects.filter(name__icontains=query) if query else []
    context = {
        'results': results,
        'query': query
    }
    return render(request, 'plants/plant_search.html', context)



@login_required
def add_review_view(request, pk):
    plant = get_object_or_404(Plant, pk=pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.plant = plant
            review.user = request.user  # ربط التعليق بالمستخدم المسجل
            review.save()
            return redirect("plant_detail", pk=pk)
    else:
        form = ReviewForm()

    return render(request, "plants/add_review.html", {"form": form, "plant": plant})


def country_plants(request, pk):
    country = get_object_or_404(Country, pk=pk)
    plants = country.plants.filter(is_published=True)
    return render(request, 'plants/country_plants.html', {
        'country': country,
        'plants': plants
    })



def plants_stats(request):
    # annotate لكل نبات مع المتوسط
    plants = Plant.objects.annotate(
        total_reviews=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    )

    # التعامل مع القيم None
    for plant in plants:
        plant.avg_rating = round(plant.avg_rating, 2) if plant.avg_rating else 0

    context = {
        'plants_stats': plants
    }
    return render(request, 'plants/plants_stats.html', context)
