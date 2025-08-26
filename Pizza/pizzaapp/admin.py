from django.contrib import admin
from .models import Pizza, Comment, Ingredient
from django.utils import timezone
from datetime import timedelta

# Register your models here.

# “Marquer comme disponible
@admin.action(description="Marquer comme disponibe")
def mark_as_available(self, request, queryset):
    queryset.update(disponible=True)
    
# Marquer comme indisponible
@admin.action(description="Marquer comme indispoible")
def mark_as_unavailable(self, request, queryset):
    queryset.update(disponible=False)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('title', 'prix', 'disponible', 'is_recent', 'created_at')
    list_filter = ('disponible',)

    filter_horizontal = ('ingredients',)
    inlines = (CommentInline,)

    search_fields = ('title',)
    ordering = ('title',)
    date_hierarchy = 'created_at'
    
    list_editable = ('disponible', 'prix')
    list_display_links = ('title',)
    
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'prix', 'disponible', 'slug', 'ingredients')
        }),
        ('Dates', {
            'fields': ('created_at',)
        }),
    )

    def is_recent(self, obj):
        return obj.created_at >= timezone.now() - timedelta(days=7)
        
    def comments_count(self, obj):
        return obj.comments.count()

    actions = (mark_as_available, mark_as_unavailable)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pizza', 'created_at')
    search_fields = ('pizza__title', 'content')