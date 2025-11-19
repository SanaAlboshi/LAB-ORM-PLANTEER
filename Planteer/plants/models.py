


from django.db import models

CATEGORY_CHOICES = [
    ('flower', 'Flower'),
    ('herb', 'Herb'),
    ('vegetable', 'Vegetable'),
    ('fruit', 'Fruit'),
]


class Plant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='plants/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name



