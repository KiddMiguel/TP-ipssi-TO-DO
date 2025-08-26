from django.db import models


# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Pizza(models.Model):
    title = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=5, decimal_places=2)
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='pizzas')

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField()
    pizza = models.ForeignKey(Pizza, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire sur {self.pizza.title}: {self.content[:20]}"
    