from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Sum

from datetime import date

from .models import Expense, Category, Income
from django.contrib.auth.models import User

def setup_admin(request):
    user = User.objects.get(username="surya")

    user.is_staff = True
    user.is_superuser = True
    user.set_password("YourNewPassword123")
    user.save()

    return redirect("/admin/")

# =====================================================
# LOGIN
# =====================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "login.html")


# =====================================================
# DASHBOARD
# =====================================================


@login_required
def dashboard(request):

    expense_list = Expense.objects.filter(
        paid_by=request.user
    ).select_related(
        "category"
    ).order_by(
        "-date",
        "-created_at"
    )

    income_list = Income.objects.filter(
        user=request.user
    ).order_by(
        "-date",
        "-created_at"
    )

    total_expenses = sum(
        expense.amount for expense in expense_list
    )

    total_income = sum(
        income.amount for income in income_list
    )

    total_balance = total_income - total_expenses

    # ==========================================
    # CURRENT MONTH + PREVIOUS MONTHS OVERVIEW
    # ==========================================

    today = timezone.localdate()

    monthly_data = []

    for i in range(6):

        # Calculate month
        month = today.month - i
        year = today.year

        while month <= 0:
            month += 12
            year -= 1

        monthly_expense = Expense.objects.filter(
            paid_by=request.user,
            date__year=year,
            date__month=month
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        monthly_income = Income.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        monthly_data.append({
            "month": date(
                year,
                month,
                1
            ).strftime("%b"),

            "income": monthly_income,
            "expense": monthly_expense,
        })

    # Oldest → newest
    monthly_data.reverse()

    return render(
        request,
        "dashboard.html",
        {
            "expense_list": expense_list,
            "income_list": income_list,
            "total_expenses": total_expenses,
            "total_income": total_income,
            "total_balance": total_balance,
            "monthly_data": monthly_data,
        }
    )
# =====================================================
# ADD CATEGORY
# =====================================================

@login_required
def add_category(request):

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        if not name:

            messages.error(
                request,
                "Please enter a category name."
            )

            return redirect("add_category")

        if Category.objects.filter(
            user=request.user,
            name__iexact=name
        ).exists():

            messages.error(
                request,
                "This category already exists."
            )

            return redirect("expenses")

        Category.objects.create(
            user=request.user,
            name=name
        )

        messages.success(
            request,
            "Category added successfully! ✅"
        )

        return redirect("expenses")

    return render(
        request,
        "add_category.html"
    )
@login_required
def expenses(request):

    categories = Category.objects.filter(
        user=request.user
    ).order_by("name")

    expense_list = Expense.objects.filter(
        paid_by=request.user
    ).select_related(
        "category"
    ).order_by(
        "-date",
        "-created_at"
    )

    return render(
        request,
        "expenses.html",
        {
            "categories": categories,
            "expense_list": expense_list,
        }
    )

# =====================================================
# ADD EXPENSE
# =====================================================

@login_required
def add_expense(request):

    categories = Category.objects.filter(
        user=request.user
    ).order_by("name")

    if request.method == "POST":

        category_id = request.POST.get("category")
        amount = request.POST.get("amount")
        description = request.POST.get(
            "description",
            ""
        ).strip()
        date = request.POST.get("date")

        if not category_id:
            messages.error(
                request,
                "Please select a category."
            )
            return redirect("add_expense")

        if not amount:
            messages.error(
                request,
                "Please enter an amount."
            )
            return redirect("add_expense")

        if not date:
            messages.error(
                request,
                "Please select a date."
            )
            return redirect("add_expense")

        category = get_object_or_404(
            Category,
            id=category_id,
            user=request.user
        )

        Expense.objects.create(
            paid_by=request.user,
            category=category,
            amount=amount,
            description=description,
            date=date
        )

        messages.success(
            request,
            "Expense added successfully! 💸"
        )

        return redirect("expenses")

    return render(
        request,
        "add_expense.html",
        {
            "categories": categories
        }
    )


# =====================================================
# INCOME PAGE
# =====================================================

@login_required
def income(request):

    income_list = Income.objects.filter(
        user=request.user
    ).order_by(
        "-date",
        "-created_at"
    )

    total_income = sum(
        item.amount for item in income_list
    )

    return render(
        request,
        "income.html",
        {
            "income_list": income_list,
            "total_income": total_income,
        }
    )


# =====================================================
# ADD INCOME
# =====================================================

@login_required
def add_income(request):

    if request.method == "POST":

        amount = request.POST.get("amount")
        description = request.POST.get(
            "description",
            ""
        ).strip()
        date = request.POST.get("date")

        if not amount:
            messages.error(
                request,
                "Please enter an amount."
            )
            return redirect("add_income")

        if not date:
            messages.error(
                request,
                "Please select a date."
            )
            return redirect("add_income")

        Income.objects.create(
            user=request.user,
            amount=amount,
            description=description,
            date=date
        )

        messages.success(
            request,
            "Income added successfully! 💰"
        )

        return redirect("income")

    return render(
        request,
        "add_income.html"
    )


# =====================================================
# DELETE INCOME
# =====================================================

@login_required
def delete_income(request, income_id):

    income = get_object_or_404(
        Income,
        id=income_id,
        user=request.user
    )

    income.delete()

    messages.success(
        request,
        "Income deleted successfully."
    )

    return redirect("income")


# =====================================================
# DELETE EXPENSE
# =====================================================

@login_required
def delete_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        paid_by=request.user
    )

    expense.delete()

    messages.success(
        request,
        "Expense deleted successfully."
    )

    return redirect("expenses")


# =====================================================
# LOGOUT
# =====================================================

def logout_view(request):

    logout(request)

    return redirect("login")