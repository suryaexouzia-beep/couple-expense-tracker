from django.contrib import admin
from django.urls import include, path
from expenses import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("expenses/", include("expenses.urls")),

    path("income/", views.income, name="income"),
    path("logout/", views.logout_view, name="logout"),
]