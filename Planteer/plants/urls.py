

from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.plants_list, name='plants_list'),  # صفحة كل النباتات
    path('new/', views.plant_create, name='plant_add'),   # إضافة نبات جديد
    path('<int:pk>/update/', views.plant_update, name='plant_edit'),  # تعديل نبتة
    path('<int:pk>/delete/', views.plant_delete, name='plant_delete'),  # حذف نبتة
    path('<int:pk>/detail/', views.plant_detail, name='plant_detail'),  # تفاصيل نبتة
    path('search/', views.plant_search, name='plant_search'),  # صفحة البحث
]
