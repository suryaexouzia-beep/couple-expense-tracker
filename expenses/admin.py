from django.contrib import admin
from .models import Category, Expense, Income


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name")
    search_fields = ("name", "user__username")
    list_filter = ("user",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "paid_by",
        "category",
        "amount",
        "description",
        "date",
        "created_at",
    )
    search_fields = (
        "description",
        "paid_by__username",
        "category__name",
    )
    list_filter = ("category", "date", "created_at")
    ordering = ("-date", "-created_at")


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "description",
        "date",
        "created_at",
    )
    search_fields = (
        "description",
        "user__username",
    )
    list_filter = ("date", "created_at")
    ordering = ("-date", "-created_at")