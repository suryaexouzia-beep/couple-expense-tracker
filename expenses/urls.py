from django.urls import path
from . import views


urlpatterns = [

    # Dashboard
    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    # Expenses
    path(
        "expenses/",
        views.expenses,
        name="expenses"
    ),

    # Add Expense
    path(
        "expenses/add/",
        views.add_expense,
        name="add_expense"
    ),

    # Add Category
    path(
        "category/add/",
        views.add_category,
        name="add_category"
    ),

    # Delete Expense
    path(
        "expenses/delete/<int:expense_id>/",
        views.delete_expense,
        name="delete_expense"
    ),

    # Income
    path(
        "income/",
        views.income,
        name="income"
    ),

    # Add Income
    path(
        "income/add/",
        views.add_income,
        name="add_income"
    ),

    # Delete Income
    path(
        "income/delete/<int:income_id>/",
        views.delete_income,
        name="delete_income"
    ),

]