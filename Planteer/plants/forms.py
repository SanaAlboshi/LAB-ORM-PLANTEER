from django import forms
from .models import Plant, CATEGORY_CHOICES
from .models import Review


class PlantForm(forms.ModelForm):
    # تعريف الـ category يدوياً
    category = forms.ChoiceField(
        choices=[('', 'Select a category ')] + list(CATEGORY_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    
    class Meta:
        model = Plant
        fields = ['name', 'description', 'image', 'category', 'is_edible', 'is_published', 'countries']
        widgets = {
            'countries': forms.CheckboxSelectMultiple(attrs={
                'class': 'countries-checkbox',
            }),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Plant name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Write description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'is_edible': forms.CheckboxInput(attrs={'class': 'form-check-center'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-center'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment'}),
        }