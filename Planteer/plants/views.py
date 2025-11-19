from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant
from .forms import PlantForm
from .models import Plant, CATEGORY_CHOICES


# عرض قائمة النباتات مع فلتر

def plants_list(request):
    plants = Plant.objects.all()
    
    # فلترة حسب الفئة أو صلاحية الأكل
    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')

    if category:
        plants = plants.filter(category=category)
    if is_edible in ['true', 'false']:
        plants = plants.filter(is_edible=(is_edible=='true'))

    context = {
        'plants': plants,
        'category': category,
        'is_edible': is_edible,
        'categories': CATEGORY_CHOICES,
        'Plant': Plant,  # تمرير الكلاس للـ template
    }
    return render(request, 'plants/plants_list.html', context)

# تفاصيل النبتة مع Related Plants
def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)

    # Related Plants: نفس الفئة، غير النبتة الحالية
    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:4]

    context = {
        'plant': plant,
        'related_plants': related_plants,
    }
    return render(request, 'plants/plant_detail.html', context)

# إضافة نبتة جديدة
def plant_create(request):
    form = PlantForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('plants_list')
    return render(request, 'plants/plant_form.html', {'form': form})

# تعديل نبتة موجودة
def plant_update(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    form = PlantForm(request.POST or None, request.FILES or None, instance=plant)
    if form.is_valid():
        form.save()
        return redirect('plant_detail', pk=plant.pk)
    return render(request, 'plants/plant_form.html', {'form': form})

# حذف نبتة
def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == 'POST':
        plant.delete()
        return redirect('plants_list')
    return render(request, 'plants/plant_delete.html', {'plant': plant})

# صفحة البحث
def plant_search(request):
    query = request.GET.get('q')
    results = Plant.objects.filter(name__icontains=query) if query else []
    context = {
        'results': results,
        'query': query
    }
    return render(request, 'plants/plant_search.html', context)
