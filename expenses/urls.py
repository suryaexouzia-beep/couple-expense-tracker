from django.urls import path
from . import views

urlpatterns = [

    path("", views.dashboard, name="dashboard"),

    # Login / Logout
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Expenses
    path("expenses/", views.expenses, name="expenses"),
    path("expenses/add/", views.add_expense, name="add_expense"),
    path("category/add/", views.add_category, name="add_category"),
    path(
        "expenses/delete/<int:expense_id>/",
        views.delete_expense,
        name="delete_expense"
    ),

    # Income
    path("income/", views.income, name="income"),
    path("income/add/", views.add_income, name="add_income"),
    path(
        "income/delete/<int:income_id>/",
        views.delete_income,
        name="delete_income"
    ),

    # Monthly Progress
    path(
        "monthly-progress/",
        views.monthly_progress,
        name="monthly_progress"
    ),

    # Charts
    path(
        "charts/",
        views.charts,
        name="charts"
    ),
]