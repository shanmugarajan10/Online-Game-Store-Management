from django.contrib import admin
from .models import Category, Game, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'release_date', 'is_featured')
    list_filter = ('category', 'release_date', 'is_featured')
    search_fields = ('title', 'developer', 'publisher')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'release_date'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('game',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__username')
    inlines = [OrderItemInline]
